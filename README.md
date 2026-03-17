# 🤖 Automated Form Filler

A beginner-friendly Python application that uses **Selenium WebDriver** to automatically fill and submit web forms on [demoqa.com](https://demoqa.com/automation-practice-form).

Built with modern tooling using **UV** (Astral's ultra-fast Python package manager).

---

## ✨ Features

- **Fills all field types:** text inputs, radio buttons, checkboxes, dropdowns, date pickers, autocomplete
- **Submits the form** and verifies the success confirmation modal
- **Automated validation tests** with pytest (positive + negative + field validation)
- **Ethical CAPTCHA handling** — only uses demo sites, never bypasses real CAPTCHAs
- **Screenshot capture** after submission
- **Clean virtual environment** — no global package pollution

---

## 📁 Project Structure

```
automated-form-filler/
├── .venv/                      # Auto-created by UV
├── pyproject.toml              # Defines project + dependencies
├── uv.lock                    # Auto-generated lock file
├── main.py                     # Main automation script
├── test_validation.py          # pytest validation tests
├── config.py                   # Form data (name, email, etc.)
├── README.md                   # This file
└── screenshots/                # Saved screenshots (auto-created)
```

---

## 🚀 Quick Start (UV — Recommended)

### Prerequisites

- **Python 3.10+** installed
- **Google Chrome** browser installed
- **UV** package manager ([install guide](https://docs.astral.sh/uv/getting-started/installation/))

### 1. Install UV (one-time only)

```bash
# Windows
winget install --id=astral-sh.uv

# macOS
brew install uv

# Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install Dependencies

```bash
# Clone/download the project, then:
uv sync
```

This creates a `.venv` and installs all dependencies automatically.

### 3. Run the Automation

```bash
uv run python main.py
```

### 4. Run Validation Tests

```bash
uv run pytest test_validation.py -v
```

---

## 🔧 Alternative Setup (pip)

If you prefer classic pip:

```bash
# Create virtual environment
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install selenium webdriver-manager pytest

# Run
python main.py

# Test
pytest test_validation.py -v
```

---

## ⚙️ Configuration

Edit `config.py` to change the form data:

```python
FIRST_NAME = "John"
LAST_NAME = "Doe"
EMAIL = "johndoe@example.com"
MOBILE_NUMBER = "9876543210"
GENDER = "Male"
DOB_DAY = "15"
DOB_MONTH = "June"
DOB_YEAR = "1995"
SUBJECTS = ["Maths", "Computer Science"]
HOBBIES = ["Sports", "Reading"]
CURRENT_ADDRESS = "123 Automation Street, Test City"
STATE = "NCR"
CITY = "Delhi"
```

---

## 🧪 Test Suite

The test suite includes:

| Category | Tests | Description |
|----------|-------|-------------|
| **Positive** | 3 tests | Valid data → successful submission |
| **Negative** | 4 tests | Missing required fields → no submission |
| **Validation** | 4 tests | Email format, mobile length, field behavior |
| **CAPTCHA** | 1 test | Verifies no CAPTCHA is present |

---

## ⚠️ Ethical Notice

This project is for **EDUCATIONAL PURPOSES ONLY**.

- ✅ Only use on demo/practice websites that explicitly allow automation
- ❌ Never bypass CAPTCHAs or abuse real services
- ❌ Never violate any website's Terms of Service
- ❌ Never use for spamming or malicious purposes

---

## 📋 Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Programming language |
| UV | Package & project manager |
| Selenium | Browser automation |
| webdriver-manager | Auto-downloads ChromeDriver |
| pytest | Testing framework |

---

## 📄 License

This project is for educational purposes. Use responsibly.
