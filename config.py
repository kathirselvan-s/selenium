"""
config.py — Form Data Configuration
=====================================
Contains all the data used to fill the automation practice form at:
https://demoqa.com/automation-practice-form

Modify these values to test different form submissions.
"""

# ─── Personal Information ───────────────────────────────────────────────────────
FIRST_NAME = "Kathirselvan"
LAST_NAME = "S"
EMAIL = "skathirselvan12@gmail.com"
MOBILE_NUMBER = "8667542949"  # Must be exactly 10 digits

# ─── Gender ─────────────────────────────────────────────────────────────────────
# Options: "Male", "Female", "Other"
GENDER = "Male"

# ─── Date of Birth ──────────────────────────────────────────────────────────────
DOB_DAY = "08"
DOB_MONTH = "September"       # Full month name (e.g., "January", "February", ...)
DOB_YEAR = "2004"

# ─── Subjects ───────────────────────────────────────────────────────────────────
# Type partial subject name; select from the autocomplete dropdown
SUBJECTS = ["Python","Machine learning","AL","NLP","Computer Science"]

# ─── Hobbies ────────────────────────────────────────────────────────────────────
# Options: "Sports", "Reading", "Music"
HOBBIES = ["Sports", "Reading","Gaming"]

# ─── Current Address ────────────────────────────────────────────────────────────
CURRENT_ADDRESS = "5/113 B2,Thathipalayam,knour,namakkal -637207"

# ─── State & City ───────────────────────────────────────────────────────────────
STATE = "Tamil Nadu"
CITY = "Namakkal"

# ─── Target URL ─────────────────────────────────────────────────────────────────
FORM_URL = "https://demoqa.com/automation-practice-form"

# ─── Timeouts (seconds) ────────────────────────────────────────────────────────
IMPLICIT_WAIT = 10
PAGE_LOAD_TIMEOUT = 30
