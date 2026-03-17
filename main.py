"""
main.py — Automated Form Filler
=================================
Uses Selenium WebDriver to automatically fill and submit the practice form at:
https://demoqa.com/automation-practice-form

Usage:
    uv run python main.py

⚠️ ETHICAL NOTICE:
    This script is for EDUCATIONAL PURPOSES ONLY.
    Only use it on demo/practice websites that explicitly allow automation.
    Never use automation to bypass CAPTCHAs, abuse services, or violate ToS.
"""

import time
import os
import shutil

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import config


def _is_chrome_available():
    """Check if Google Chrome is installed and accessible."""
    # Check common Chrome paths on Windows
    chrome_paths = [
        os.path.join(os.environ.get("PROGRAMFILES", ""), "Google", "Chrome", "Application", "chrome.exe"),
        os.path.join(os.environ.get("PROGRAMFILES(X86)", ""), "Google", "Chrome", "Application", "chrome.exe"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Google", "Chrome", "Application", "chrome.exe"),
    ]
    for path in chrome_paths:
        if os.path.isfile(path):
            return True
    # Also check if 'chrome' is on PATH
    return shutil.which("chrome") is not None or shutil.which("google-chrome") is not None


def _is_edge_available():
    """Check if Microsoft Edge is installed and accessible."""
    edge_paths = [
        os.path.join(os.environ.get("PROGRAMFILES", ""), "Microsoft", "Edge", "Application", "msedge.exe"),
        os.path.join(os.environ.get("PROGRAMFILES(X86)", ""), "Microsoft", "Edge", "Application", "msedge.exe"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Edge", "Application", "msedge.exe"),
    ]
    for path in edge_paths:
        if os.path.isfile(path):
            return True
    return shutil.which("msedge") is not None


def create_driver():
    """
    Create and configure the WebDriver instance.
    Auto-detects the available browser:
      1. Google Chrome (preferred)
      2. Microsoft Edge (fallback)
    Selenium 4.6+ includes built-in Selenium Manager for automatic driver management.
    """
    common_args = [
        "--start-maximized",
        "--disable-notifications",
        "--disable-infobars",
        "--log-level=3",
    ]

    # ── Try Chrome first ─────────────────────────────────────────────────────
    if _is_chrome_available():
        print("🔧 Setting up Chrome WebDriver...")
        from selenium.webdriver.chrome.options import Options as ChromeOptions

        options = ChromeOptions()
        for arg in common_args:
            options.add_argument(arg)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        # Selenium Manager handles driver download automatically
        driver = webdriver.Chrome(options=options)

    # ── Fallback to Edge ─────────────────────────────────────────────────────
    elif _is_edge_available():
        print("🔧 Chrome not found. Setting up Microsoft Edge WebDriver...")
        from selenium.webdriver.edge.options import Options as EdgeOptions

        options = EdgeOptions()
        for arg in common_args:
            options.add_argument(arg)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        # Selenium Manager handles driver download automatically
        driver = webdriver.Edge(options=options)

    else:
        raise RuntimeError(
            "❌ No supported browser found!\n"
            "   Please install Google Chrome or Microsoft Edge."
        )

    # Set timeouts
    driver.implicitly_wait(config.IMPLICIT_WAIT)
    driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)

    print("✅ WebDriver is ready!\n")
    return driver


def remove_ads_and_footer(driver):
    """
    Remove intrusive ad banners and fixed footer from the demoqa page
    so they don't block our form interactions.
    """
    try:
        driver.execute_script("""
            // Remove the fixed footer
            var footer = document.getElementById('fixedban');
            if (footer) footer.remove();

            // Remove any ad frames
            var ads = document.querySelectorAll('iframe, #Ad\\.Plus-728x90, .ad');
            ads.forEach(function(ad) { ad.remove(); });

            // Remove the site footer
            var siteFooter = document.querySelector('footer');
            if (siteFooter) siteFooter.remove();
        """)
    except Exception:
        pass  # Ads may not always be present


def scroll_to_element(driver, element):
    """Scroll element into view before interacting with it."""
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
        element
    )
    time.sleep(0.3)


def fill_text_field(driver, css_selector, value, field_name):
    """Fill a text input field and log the action."""
    element = driver.find_element(By.CSS_SELECTOR, css_selector)
    scroll_to_element(driver, element)
    element.clear()
    element.send_keys(value)
    print(f"  ✏️  Filled '{field_name}': {value}")


def select_gender(driver, gender):
    """Select a gender radio button by clicking its label."""
    gender_map = {"Male": "gender-radio-1", "Female": "gender-radio-2", "Other": "gender-radio-3"}
    radio_id = gender_map.get(gender)
    if not radio_id:
        print(f"  ⚠️  Unknown gender: {gender}")
        return

    # The actual radio input is hidden; click its label instead
    label = driver.find_element(By.CSS_SELECTOR, f"label[for='{radio_id}']")
    scroll_to_element(driver, label)
    label.click()
    print(f"  🔘 Selected gender: {gender}")


def set_date_of_birth(driver, day, month, year):
    """
    Set the date of birth using the date picker widget.
    Opens the picker, selects year → month → day.
    """
    dob_input = driver.find_element(By.ID, "dateOfBirthInput")
    scroll_to_element(driver, dob_input)
    dob_input.click()
    time.sleep(0.5)

    # Select Year
    year_dropdown = driver.find_element(
        By.CSS_SELECTOR, ".react-datepicker__year-select"
    )
    year_dropdown.click()
    year_option = year_dropdown.find_element(
        By.CSS_SELECTOR, f"option[value='{year}']"
    )
    year_option.click()
    time.sleep(0.3)

    # Select Month
    month_map = {
        "January": "0", "February": "1", "March": "2", "April": "3",
        "May": "4", "June": "5", "July": "6", "August": "7",
        "September": "8", "October": "9", "November": "10", "December": "11"
    }
    month_value = month_map.get(month, "0")
    month_dropdown = driver.find_element(
        By.CSS_SELECTOR, ".react-datepicker__month-select"
    )
    month_dropdown.click()
    month_option = month_dropdown.find_element(
        By.CSS_SELECTOR, f"option[value='{month_value}']"
    )
    month_option.click()
    time.sleep(0.3)

    # Select Day
    # Ensure we pick the exact day, not from prev/next month
    day_elements = driver.find_elements(
        By.CSS_SELECTOR,
        ".react-datepicker__day:not(.react-datepicker__day--outside-month)"
    )
    for day_el in day_elements:
        if day_el.text.strip() == str(int(day)):
            day_el.click()
            break
    print(f"  📅 Set date of birth: {day} {month} {year}")


def add_subjects(driver, subjects):
    """
    Type each subject into the subjects autocomplete and select from dropdown.
    """
    subject_input = driver.find_element(By.ID, "subjectsInput")
    scroll_to_element(driver, subject_input)

    for subject in subjects:
        subject_input.send_keys(subject)
        time.sleep(0.5)

        # Wait for autocomplete suggestion and click it
        try:
            suggestion = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".subjects-auto-complete__option")
                )
            )
            suggestion.click()
            print(f"  📚 Added subject: {subject}")
        except Exception:
            # Fallback: press Enter to select the first suggestion
            subject_input.send_keys(Keys.RETURN)
            print(f"  📚 Added subject (via Enter): {subject}")

        time.sleep(0.3)


def select_hobbies(driver, hobbies):
    """Select hobby checkboxes by clicking their labels."""
    hobby_map = {
        "Sports": "hobbies-checkbox-1",
        "Reading": "hobbies-checkbox-2",
        "Music": "hobbies-checkbox-3"
    }
    for hobby in hobbies:
        checkbox_id = hobby_map.get(hobby)
        if checkbox_id:
            label = driver.find_element(By.CSS_SELECTOR, f"label[for='{checkbox_id}']")
            scroll_to_element(driver, label)
            label.click()
            print(f"  ☑️  Selected hobby: {hobby}")


def fill_address(driver, address):
    """Fill the current address textarea."""
    textarea = driver.find_element(By.ID, "currentAddress")
    scroll_to_element(driver, textarea)
    textarea.clear()
    textarea.send_keys(address)
    print(f"  🏠 Filled address: {address[:40]}...")


def select_state_and_city(driver, state, city):
    """
    Select State and City from the react-select dropdowns.
    These are custom dropdowns (not standard <select> elements).
    """
    # Select State
    state_container = driver.find_element(By.ID, "state")
    scroll_to_element(driver, state_container)
    state_container.click()
    time.sleep(0.5)

    state_option = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//div[contains(@class, 'option') and text()='{state}']")
        )
    )
    state_option.click()
    print(f"  🗺️  Selected state: {state}")
    time.sleep(0.5)

    # Select City
    city_container = driver.find_element(By.ID, "stateCity-wrapper")
    city_dropdown = city_container.find_element(By.ID, "city")
    scroll_to_element(driver, city_dropdown)
    city_dropdown.click()
    time.sleep(0.5)

    city_option = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//div[contains(@class, 'option') and text()='{city}']")
        )
    )
    city_option.click()
    print(f"  🏙️  Selected city: {city}")


def submit_form(driver):
    """Click the Submit button."""
    submit_btn = driver.find_element(By.ID, "submit")
    scroll_to_element(driver, submit_btn)

    # Use JavaScript click as a fallback in case the button is overlapped
    driver.execute_script("arguments[0].click();", submit_btn)
    print("\n  🚀 Form submitted!")


def verify_submission(driver):
    """
    Check if the success modal appeared after form submission.
    Returns True if the 'Thanks for submitting the form' modal is displayed.
    """
    try:
        modal = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.ID, "example-modal-sizes-title-lg")
            )
        )
        modal_text = modal.text
        print(f"\n  🎉 SUCCESS! Modal says: '{modal_text}'")

        # Print all submitted values from the modal table
        table_rows = driver.find_elements(By.CSS_SELECTOR, ".modal-body table tbody tr")
        if table_rows:
            print("\n  📋 Submitted Data:")
            print("  " + "─" * 50)
            for row in table_rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) == 2:
                    print(f"    {cells[0].text:<20} │ {cells[1].text}")
            print("  " + "─" * 50)

        return True

    except Exception as e:
        print(f"\n  ❌ Submission verification FAILED: {e}")
        return False


def handle_captcha():
    """
    ⚠️ ETHICAL CAPTCHA HANDLING — SIMULATION ONLY
    ═══════════════════════════════════════════════

    This function is a PLACEHOLDER to demonstrate ethical CAPTCHA handling.

    In a real-world scenario:
      ❌ DO NOT use automated CAPTCHA-solving services
      ❌ DO NOT bypass CAPTCHA mechanisms
      ❌ DO NOT use OCR or ML to solve CAPTCHAs without consent

    CAPTCHAs exist to protect websites from abuse.
    If a form has a CAPTCHA, it means automated submission is NOT welcome.

    For educational/testing purposes:
      ✅ Use demo sites that don't have CAPTCHAs (like demoqa.com)
      ✅ Ask the site owner for an API key or test mode
      ✅ Use mock CAPTCHAs in your own test environment

    The demoqa.com practice form does NOT have a CAPTCHA,
    so this function simply logs a message and returns.
    """
    print("  🔒 CAPTCHA check: No CAPTCHA present on this demo form.")
    print("     (See handle_captcha() docstring for ethical guidelines)")
    return True


def save_screenshot(driver, filename="form_submitted.png"):
    """Save a screenshot after form submission."""
    screenshots_dir = os.path.join(os.path.dirname(__file__), "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)
    filepath = os.path.join(screenshots_dir, filename)
    driver.save_screenshot(filepath)
    print(f"  📸 Screenshot saved: {filepath}")


def run_automation():
    """
    Main automation workflow:
    1. Launch browser & navigate to form
    2. Fill all fields
    3. Handle CAPTCHA (simulated)
    4. Submit form
    5. Verify submission
    6. Save screenshot
    """
    driver = None

    try:
        # ── Step 1: Setup ────────────────────────────────────────────────────
        print("=" * 60)
        print("  🤖 AUTOMATED FORM FILLER")
        print("  Target: demoqa.com/automation-practice-form")
        print("=" * 60)

        driver = create_driver()

        print(f"🌐 Navigating to: {config.FORM_URL}")
        driver.get(config.FORM_URL)
        time.sleep(2)

        # Remove ads/footer that might block interactions
        remove_ads_and_footer(driver)

        # ── Step 2: Fill the form ────────────────────────────────────────────
        print("\n📝 Filling form fields...\n")

        fill_text_field(driver, "#firstName", config.FIRST_NAME, "First Name")
        fill_text_field(driver, "#lastName", config.LAST_NAME, "Last Name")
        fill_text_field(driver, "#userEmail", config.EMAIL, "Email")

        select_gender(driver, config.GENDER)

        fill_text_field(driver, "#userNumber", config.MOBILE_NUMBER, "Mobile")

        set_date_of_birth(driver, config.DOB_DAY, config.DOB_MONTH, config.DOB_YEAR)

        add_subjects(driver, config.SUBJECTS)

        select_hobbies(driver, config.HOBBIES)

        # ── Step 3: CAPTCHA handling (ethical simulation) ────────────────────
        print()
        handle_captcha()
        print()

        fill_address(driver, config.CURRENT_ADDRESS)

        select_state_and_city(driver, config.STATE, config.CITY)

        # ── Step 4: Submit ───────────────────────────────────────────────────
        print()
        submit_form(driver)

        # ── Step 5: Verify ───────────────────────────────────────────────────
        time.sleep(1)
        success = verify_submission(driver)

        # ── Step 6: Screenshot ───────────────────────────────────────────────
        save_screenshot(driver)

        if success:
            print("\n✅ Automation completed successfully! 🎉")
        else:
            print("\n⚠️ Automation completed but verification failed.")

        # Pause briefly so the user can see the result
        time.sleep(3)

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        if driver:
            save_screenshot(driver, "error_screenshot.png")
        raise

    finally:
        if driver:
            print("\n🔒 Closing browser...")
            driver.quit()
            print("👋 Done!")


# ─── Entry Point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_automation()
