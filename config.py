"""
config.py — Form Data Configuration
=====================================
Contains all the data used to fill the automation practice form at:
https://demoqa.com/automation-practice-form

Modify these values to test different form submissions.
"""

# ─── Personal Information ───────────────────────────────────────────────────────
FIRST_NAME = "John"
LAST_NAME = "Doe"
EMAIL = "johndoe@example.com"
MOBILE_NUMBER = "9876543210"  # Must be exactly 10 digits

# ─── Gender ─────────────────────────────────────────────────────────────────────
# Options: "Male", "Female", "Other"
GENDER = "Male"

# ─── Date of Birth ──────────────────────────────────────────────────────────────
DOB_DAY = "15"
DOB_MONTH = "June"       # Full month name (e.g., "January", "February", ...)
DOB_YEAR = "1995"

# ─── Subjects ───────────────────────────────────────────────────────────────────
# Type partial subject name; select from the autocomplete dropdown
SUBJECTS = ["Maths", "Computer Science"]

# ─── Hobbies ────────────────────────────────────────────────────────────────────
# Options: "Sports", "Reading", "Music"
HOBBIES = ["Sports", "Reading"]

# ─── Current Address ────────────────────────────────────────────────────────────
CURRENT_ADDRESS = "123 Automation Street, Test City, QA State 560001"

# ─── State & City ───────────────────────────────────────────────────────────────
STATE = "NCR"
CITY = "Delhi"

# ─── Target URL ─────────────────────────────────────────────────────────────────
FORM_URL = "https://demoqa.com/automation-practice-form"

# ─── Timeouts (seconds) ────────────────────────────────────────────────────────
IMPLICIT_WAIT = 10
PAGE_LOAD_TIMEOUT = 30
