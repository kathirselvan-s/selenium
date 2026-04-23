# 🤖 Automated Form Filler

A professional Python application that uses **Selenium WebDriver** to automatically fill and submit web forms on [demoqa.com](https://demoqa.com/automation-practice-form).

Built with modern tooling using **UV** (Astral's ultra-fast Python package manager), this project demonstrates robust automation patterns, including custom element handling, automatic browser detection, and ethical scraping practices.

---

## ✨ Features

- **Multi-Browser Support:** Auto-detects and uses Google Chrome or Microsoft Edge.
- **Complex Field Handling:** Automates text inputs, radio buttons, checkboxes, custom React-select dropdowns, date pickers, and autocomplete fields.
- **Robust Interactions:** Implements smooth scrolling and explicit waits to ensure elements are interactable.
- **Success Verification:** Automatically parses the post-submission modal to verify data integrity.
- **Automated Validation:** Comprehensive test suite with positive, negative, and edge-case scenarios.
- **Screenshot Capture:** Saves visual proof of successful submissions or error states.
- **Ethical Design:** Includes built-in guidelines and placeholders for responsible automation.

---

## 📁 Project Structure

```text
automated-form-filler/
├── .venv/                      # Auto-managed virtual environment
├── config.py                   # Form data configuration (name, email, etc.)
├── main.py                     # Primary automation engine
├── test_validation.py          # Pytest-based validation suite
├── pyproject.toml              # Project metadata & dependencies
├── uv.lock                    # Deterministic dependency lock file
├── screenshots/                # Automated capture storage
└── README.md                   # Project documentation
```

---

## 🚀 Quick Start (Recommended)

### Prerequisites

- **Python 3.10+**
- **Google Chrome** or **Microsoft Edge**
- **UV** package manager ([Installation Guide](https://docs.astral.sh/uv/getting-started/installation/))

### 1. Setup Environment

```bash
# Clone the repository and sync dependencies
uv sync
```

### 2. Run Automation

```bash
uv run python main.py
```

### 3. Run Tests

```bash
uv run pytest test_validation.py -v
```

---

## ⚙️ Configuration

The application is data-driven. Edit `config.py` to customize the submission data. Below is the current sample data configured in the project:

```python
# Personal Information
FIRST_NAME = "Kathirselvan"
LAST_NAME = "S"
EMAIL = "skathirselvan12@gmail.com"
MOBILE_NUMBER = "8667542949"

# Form Selections
GENDER = "Male"
DOB_DAY = "08"
DOB_MONTH = "September"
DOB_YEAR = "2004"

# Multi-select Fields
SUBJECTS = ["Python", "Machine learning", "AL", "NLP", "Computer Science"]
HOBBIES = ["Sports", "Reading", "Gaming"]

# Address & Location
CURRENT_ADDRESS = "5/113 B2, Thathipalayam, knour, namakkal - 637207"
STATE = "Tamil Nadu"
CITY = "Namakkal"
```

---

## 🛠️ Tech Stack & Tools

| Tool | Purpose |
|------|---------|
| **Python 3.10+** | Core programming logic |
| **UV** | High-performance dependency management |
| **Selenium 4.20+** | Browser automation & DOM interaction |
| **Selenium Manager** | Zero-config driver management (automatic) |
| **Pytest** | Industrial-grade testing framework |

---

## ⚖️ Ethical Automation Guidelines

This project strictly adheres to ethical automation practices:

1. **Targeting:** Only used on dedicated practice/sandbox domains.
2. **CAPTCHA:** No automated bypasses; follows "Human-in-the-loop" or "Sandbox-only" principles.
3. **Resource Usage:** Implements throttled interactions to avoid overwhelming target servers.
4. **Transparency:** Clearly identifies as an automated agent via user-agent or logging.

---

## 📄 License

Educational Use Only. Built with ❤️ for the Selenium community.
