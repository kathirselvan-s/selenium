"""
app.py — Flask Web UI for Automated Form Filler
=================================================
Provides a web interface to configure and trigger the Selenium automation.
"""

import json
import queue
import subprocess
import sys
import threading
import time
import re
import os
from pathlib import Path

from flask import Flask, Response, jsonify, render_template, request, stream_with_context

# ── App Setup ────────────────────────────────────────────────────────────────
app = Flask(__name__)
BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config.py"

# ── Config Read/Write Helpers ────────────────────────────────────────────────

def read_config() -> dict:
    """Parse config.py and return a dict of key→value pairs."""
    cfg = {}
    text = CONFIG_FILE.read_text(encoding="utf-8")
    patterns = {
        "FIRST_NAME":       r'FIRST_NAME\s*=\s*"([^"]*)"',
        "LAST_NAME":        r'LAST_NAME\s*=\s*"([^"]*)"',
        "EMAIL":            r'EMAIL\s*=\s*"([^"]*)"',
        "MOBILE_NUMBER":    r'MOBILE_NUMBER\s*=\s*"([^"]*)"',
        "GENDER":           r'GENDER\s*=\s*"([^"]*)"',
        "DOB_DAY":          r'DOB_DAY\s*=\s*"([^"]*)"',
        "DOB_MONTH":        r'DOB_MONTH\s*=\s*"([^"]*)"',
        "DOB_YEAR":         r'DOB_YEAR\s*=\s*"([^"]*)"',
        "CURRENT_ADDRESS":  r'CURRENT_ADDRESS\s*=\s*"([^"]*)"',
        "STATE":            r'STATE\s*=\s*"([^"]*)"',
        "CITY":             r'CITY\s*=\s*"([^"]*)"',
        "FORM_URL":         r'FORM_URL\s*=\s*"([^"]*)"',
        "IMPLICIT_WAIT":    r'IMPLICIT_WAIT\s*=\s*(\d+)',
        "PAGE_LOAD_TIMEOUT":r'PAGE_LOAD_TIMEOUT\s*=\s*(\d+)',
    }
    for key, pattern in patterns.items():
        m = re.search(pattern, text)
        cfg[key] = m.group(1) if m else ""

    # Lists
    for list_key in ("SUBJECTS", "HOBBIES"):
        m = re.search(rf'{list_key}\s*=\s*\[([^\]]*)\]', text)
        if m:
            raw = m.group(1)
            items = [i.strip().strip('"').strip("'") for i in raw.split(",") if i.strip()]
            cfg[list_key] = items
        else:
            cfg[list_key] = []
    return cfg


def write_config(data: dict):
    """Rewrite config.py with the provided data."""
    subjects_repr = ", ".join(f'"{s}"' for s in data.get("SUBJECTS", []))
    hobbies_repr  = ", ".join(f'"{h}"' for h in data.get("HOBBIES", []))

    content = f'''"""
config.py — Form Data Configuration
=====================================
Contains all the data used to fill the automation practice form.
Modify these values to test different form submissions.
"""

# ─── Personal Information ───────────────────────────────────────────────────────
FIRST_NAME = "{data.get('FIRST_NAME', '')}"
LAST_NAME = "{data.get('LAST_NAME', '')}"
EMAIL = "{data.get('EMAIL', '')}"
MOBILE_NUMBER = "{data.get('MOBILE_NUMBER', '')}"  # Must be exactly 10 digits

# ─── Gender ─────────────────────────────────────────────────────────────────────
# Options: "Male", "Female", "Other"
GENDER = "{data.get('GENDER', 'Male')}"

# ─── Date of Birth ──────────────────────────────────────────────────────────────
DOB_DAY = "{data.get('DOB_DAY', '')}"
DOB_MONTH = "{data.get('DOB_MONTH', '')}"       # Full month name (e.g., "January", "February", ...)
DOB_YEAR = "{data.get('DOB_YEAR', '')}"

# ─── Subjects ───────────────────────────────────────────────────────────────────
# Type partial subject name; select from the autocomplete dropdown
SUBJECTS = [{subjects_repr}]

# ─── Hobbies ────────────────────────────────────────────────────────────────────
# Options: "Sports", "Reading", "Music"
HOBBIES = [{hobbies_repr}]

# ─── Current Address ────────────────────────────────────────────────────────────
CURRENT_ADDRESS = "{data.get('CURRENT_ADDRESS', '')}"

# ─── State & City ───────────────────────────────────────────────────────────────
STATE = "{data.get('STATE', '')}"
CITY = "{data.get('CITY', '')}"

# ─── Target URL ─────────────────────────────────────────────────────────────────
FORM_URL = "{data.get('FORM_URL', 'https://demoqa.com/automation-practice-form')}"

# ─── Timeouts (seconds) ────────────────────────────────────────────────────────
IMPLICIT_WAIT = {int(data.get('IMPLICIT_WAIT', 10))}
PAGE_LOAD_TIMEOUT = {int(data.get('PAGE_LOAD_TIMEOUT', 30))}
'''
    CONFIG_FILE.write_text(content, encoding="utf-8")


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/config", methods=["GET"])
def get_config():
    try:
        cfg = read_config()
        return jsonify({"success": True, "config": cfg})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/config", methods=["POST"])
def save_config():
    try:
        data = request.get_json()
        write_config(data)
        return jsonify({"success": True, "message": "Configuration saved successfully!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/run", methods=["POST"])
def run_automation():
    """Stream automation logs via Server-Sent Events."""
    data = request.get_json() or {}

    # Save config first if data provided
    if data:
        try:
            write_config(data)
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    log_queue: queue.Queue = queue.Queue()

    def run_script():
        try:
            python_exe = sys.executable
            proc = subprocess.Popen(
                [python_exe, str(BASE_DIR / "main.py")],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                cwd=str(BASE_DIR),
            )
            for line in proc.stdout:
                log_queue.put(("log", line.rstrip()))
            proc.wait()
            code = proc.returncode
            if code == 0:
                log_queue.put(("done", "✅ Automation completed successfully!"))
            else:
                log_queue.put(("error", f"❌ Process exited with code {code}"))
        except Exception as e:
            log_queue.put(("error", f"❌ Failed to start: {e}"))
        finally:
            log_queue.put(("end", ""))

    thread = threading.Thread(target=run_script, daemon=True)
    thread.start()

    def generate():
        while True:
            try:
                kind, msg = log_queue.get(timeout=120)
                payload = json.dumps({"type": kind, "message": msg})
                yield f"data: {payload}\n\n"
                if kind in ("done", "error", "end"):
                    break
            except queue.Empty:
                yield f"data: {json.dumps({'type': 'error', 'message': 'Timeout waiting for process'})}\n\n"
                break

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


if __name__ == "__main__":
    print("Starting Form Filler UI at http://127.0.0.1:5000")
    app.run(debug=False, host="127.0.0.1", port=5000, threaded=True)
