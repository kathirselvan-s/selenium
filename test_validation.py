"""
test_validation.py — Automated Validation Tests
==================================================
Uses pytest + Selenium to validate the automation practice form at demoqa.com.

Includes:
  - Positive tests (valid data → form submits successfully)
  - Negative tests (missing required fields → form does NOT submit)
  - Field validation tests (email format, mobile number length)

Usage:
    uv run pytest test_validation.py -v

⚠️ ETHICAL NOTICE:
    These tests are for EDUCATIONAL PURPOSES ONLY on public demo sites.
"""

import time
import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import config
from main import create_driver


# ─── Fixtures ───────────────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def driver():
    """
    Create a fresh WebDriver instance for each test.
    Uses the shared create_driver() function which auto-detects Chrome or Edge.
    Navigates to the form URL and cleans up ads/footer.
    Yields the driver and quits after the test completes.
    """
    browser = create_driver()

    # Navigate to the form
    browser.get(config.FORM_URL)
    time.sleep(2)

    # Remove ads and fixed footer
    _remove_ads(browser)

    yield browser

    browser.quit()


def _remove_ads(driver):
    """Remove intrusive ads and footer from the page."""
    try:
        driver.execute_script("""
            var footer = document.getElementById('fixedban');
            if (footer) footer.remove();
            var ads = document.querySelectorAll('iframe, .ad');
            ads.forEach(function(ad) { ad.remove(); });
            var siteFooter = document.querySelector('footer');
            if (siteFooter) siteFooter.remove();
        """)
    except Exception:
        pass


def _scroll_and_click(driver, element):
    """Scroll to an element and click it."""
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", element
    )
    time.sleep(0.3)
    element.click()


def _fill_minimum_required_fields(driver):
    """
    Fill only the minimum required fields for a valid submission:
    First Name, Last Name, Gender, and Mobile Number.
    """
    driver.find_element(By.CSS_SELECTOR, "#firstName").send_keys(config.FIRST_NAME)
    driver.find_element(By.CSS_SELECTOR, "#lastName").send_keys(config.LAST_NAME)

    # Gender
    gender_label = driver.find_element(By.CSS_SELECTOR, "label[for='gender-radio-1']")
    _scroll_and_click(driver, gender_label)

    driver.find_element(By.CSS_SELECTOR, "#userNumber").send_keys(config.MOBILE_NUMBER)


def _submit_form(driver):
    """Submit the form using JavaScript click."""
    submit_btn = driver.find_element(By.ID, "submit")
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", submit_btn
    )
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", submit_btn)


def _is_submission_successful(driver, timeout=5):
    """
    Check if the success modal appears within the given timeout.
    Returns True if modal is displayed, False otherwise.
    """
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(
                (By.ID, "example-modal-sizes-title-lg")
            )
        )
        return True
    except TimeoutException:
        return False


def _get_modal_data(driver):
    """
    Extract submitted data from the success modal table.
    Returns a dict like {"Student Name": "Kathirselvan", "Student Email": "skathirselvan12@gmail.com", ...}
    """
    data = {}
    try:
        rows = driver.find_elements(By.CSS_SELECTOR, ".modal-body table tbody tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) == 2:
                data[cells[0].text.strip()] = cells[1].text.strip()
    except Exception:
        pass
    return data


# ─── POSITIVE TESTS ────────────────────────────────────────────────────────────

class TestPositiveSubmission:
    """Tests that verify the form submits correctly with valid data."""

    def test_submit_with_required_fields_only(self, driver):
        """
        Form should submit successfully with just the required fields:
        First Name, Last Name, Gender, Mobile Number.
        """
        _fill_minimum_required_fields(driver)
        _submit_form(driver)
        time.sleep(1)

        assert _is_submission_successful(driver), \
            "Form should submit successfully with required fields filled"

    def test_submitted_data_matches_input(self, driver):
        """
        Verify that the data shown in the success modal matches what we typed.
        """
        _fill_minimum_required_fields(driver)

        # Also add email so we can verify it in the modal
        driver.find_element(By.CSS_SELECTOR, "#userEmail").send_keys(config.EMAIL)

        _submit_form(driver)
        time.sleep(1)

        assert _is_submission_successful(driver), "Form should submit successfully"

        modal_data = _get_modal_data(driver)

        expected_name = f"{config.FIRST_NAME} {config.LAST_NAME}"
        assert modal_data.get("Student Name") == expected_name, \
            f"Expected name '{expected_name}', got '{modal_data.get('Student Name')}'"

        assert modal_data.get("Student Email") == config.EMAIL, \
            f"Expected email '{config.EMAIL}', got '{modal_data.get('Student Email')}'"

        assert modal_data.get("Mobile") == config.MOBILE_NUMBER, \
            f"Expected mobile '{config.MOBILE_NUMBER}', got '{modal_data.get('Mobile')}'"

    def test_submit_with_all_fields(self, driver):
        """
        Form should submit successfully when ALL fields are filled,
        including optional ones like subjects, hobbies, address, state/city.
        """
        # Required fields
        _fill_minimum_required_fields(driver)
        driver.find_element(By.CSS_SELECTOR, "#userEmail").send_keys(config.EMAIL)

        # Subjects
        subject_input = driver.find_element(By.ID, "subjectsInput")
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", subject_input
        )
        for subject in config.SUBJECTS:
            subject_input.send_keys(subject)
            time.sleep(0.5)
            try:
                suggestion = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, ".subjects-auto-complete__option")
                    )
                )
                suggestion.click()
            except Exception:
                subject_input.send_keys(Keys.RETURN)
            time.sleep(0.3)

        # Hobbies
        for hobby_id in ["hobbies-checkbox-1", "hobbies-checkbox-2"]:
            label = driver.find_element(By.CSS_SELECTOR, f"label[for='{hobby_id}']")
            _scroll_and_click(driver, label)

        # Address
        address_field = driver.find_element(By.ID, "currentAddress")
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", address_field
        )
        address_field.send_keys(config.CURRENT_ADDRESS)

        # State
        state_container = driver.find_element(By.ID, "state")
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", state_container
        )
        state_container.click()
        time.sleep(0.5)
        state_option = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//div[contains(@class, 'option') and text()='{config.STATE}']")
            )
        )
        state_option.click()
        time.sleep(0.5)

        # City
        city_container = driver.find_element(By.ID, "city")
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", city_container
        )
        city_container.click()
        time.sleep(0.5)
        city_option = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//div[contains(@class, 'option') and text()='{config.CITY}']")
            )
        )
        city_option.click()

        _submit_form(driver)
        time.sleep(1)

        assert _is_submission_successful(driver), \
            "Form should submit with all fields filled"

        # Verify some of the data in the modal
        modal_data = _get_modal_data(driver)
        assert config.STATE in modal_data.get("State and City", ""), \
            f"State '{config.STATE}' should appear in modal"
        assert config.CITY in modal_data.get("State and City", ""), \
            f"City '{config.CITY}' should appear in modal"


# ─── NEGATIVE TESTS ────────────────────────────────────────────────────────────

class TestNegativeSubmission:
    """Tests that verify the form does NOT submit with missing/invalid data."""

    def test_submit_empty_form(self, driver):
        """
        Submitting the form with no data filled should NOT show success modal.
        The form has required fields (First Name, Last Name, Gender, Mobile).
        """
        _submit_form(driver)
        time.sleep(1)

        assert not _is_submission_successful(driver, timeout=3), \
            "Empty form should NOT submit successfully"

    def test_submit_without_first_name(self, driver):
        """Form should not submit without First Name."""
        # Fill everything except first name
        driver.find_element(By.CSS_SELECTOR, "#lastName").send_keys(config.LAST_NAME)
        gender_label = driver.find_element(By.CSS_SELECTOR, "label[for='gender-radio-1']")
        _scroll_and_click(driver, gender_label)
        driver.find_element(By.CSS_SELECTOR, "#userNumber").send_keys(config.MOBILE_NUMBER)

        _submit_form(driver)
        time.sleep(1)

        assert not _is_submission_successful(driver, timeout=3), \
            "Form without first name should NOT submit"

    def test_submit_without_gender(self, driver):
        """Form should not submit without selecting a gender."""
        driver.find_element(By.CSS_SELECTOR, "#firstName").send_keys(config.FIRST_NAME)
        driver.find_element(By.CSS_SELECTOR, "#lastName").send_keys(config.LAST_NAME)
        driver.find_element(By.CSS_SELECTOR, "#userNumber").send_keys(config.MOBILE_NUMBER)

        _submit_form(driver)
        time.sleep(1)

        assert not _is_submission_successful(driver, timeout=3), \
            "Form without gender should NOT submit"

    def test_submit_without_mobile(self, driver):
        """Form should not submit without mobile number."""
        driver.find_element(By.CSS_SELECTOR, "#firstName").send_keys(config.FIRST_NAME)
        driver.find_element(By.CSS_SELECTOR, "#lastName").send_keys(config.LAST_NAME)
        gender_label = driver.find_element(By.CSS_SELECTOR, "label[for='gender-radio-1']")
        _scroll_and_click(driver, gender_label)

        _submit_form(driver)
        time.sleep(1)

        assert not _is_submission_successful(driver, timeout=3), \
            "Form without mobile number should NOT submit"


# ─── FIELD VALIDATION TESTS ────────────────────────────────────────────────────

class TestFieldValidation:
    """Tests that verify field-level validation behavior."""

    def test_invalid_email_format(self, driver):
        """
        An invalid email should prevent successful submission
        (the form validates email format client-side).
        """
        _fill_minimum_required_fields(driver)

        # Type an invalid email
        email_field = driver.find_element(By.CSS_SELECTOR, "#userEmail")
        email_field.send_keys("not-a-valid-email")

        _submit_form(driver)
        time.sleep(1)

        assert not _is_submission_successful(driver, timeout=3), \
            "Invalid email should prevent form submission"

    def test_short_mobile_number(self, driver):
        """
        Mobile number must be 10 digits. A shorter number should prevent submission.
        """
        driver.find_element(By.CSS_SELECTOR, "#firstName").send_keys(config.FIRST_NAME)
        driver.find_element(By.CSS_SELECTOR, "#lastName").send_keys(config.LAST_NAME)
        gender_label = driver.find_element(By.CSS_SELECTOR, "label[for='gender-radio-1']")
        _scroll_and_click(driver, gender_label)

        # Only 5 digits instead of 10
        driver.find_element(By.CSS_SELECTOR, "#userNumber").send_keys("12345")

        _submit_form(driver)
        time.sleep(1)

        assert not _is_submission_successful(driver, timeout=3), \
            "Short mobile number should prevent submission"

    def test_first_name_field_accepts_text(self, driver):
        """Verify the first name field correctly accepts and displays text."""
        first_name_field = driver.find_element(By.CSS_SELECTOR, "#firstName")
        first_name_field.send_keys("TestUser")

        actual_value = first_name_field.get_attribute("value")
        assert actual_value == "TestUser", \
            f"Expected 'TestUser', got '{actual_value}'"

    def test_mobile_field_maxlength(self, driver):
        """
        The mobile field should only accept 10 digits max.
        Typing more than 10 digits should be truncated by the field.
        """
        mobile_field = driver.find_element(By.CSS_SELECTOR, "#userNumber")
        mobile_field.send_keys("12345678901234")  # 14 digits

        actual_value = mobile_field.get_attribute("value")
        assert len(actual_value) == 10, \
            f"Mobile field should max out at 10 digits, got {len(actual_value)}: '{actual_value}'"


# ─── CAPTCHA AWARENESS TEST ────────────────────────────────────────────────────

class TestCaptchaAwareness:
    """
    Tests to demonstrate ethical CAPTCHA handling awareness.
    The demoqa form does NOT have a CAPTCHA — these tests document the approach.
    """

    def test_no_captcha_present(self, driver):
        """
        Verify that the demo form does NOT have a CAPTCHA element.
        If a CAPTCHA were present, automation should pause or skip.
        """
        captcha_selectors = [
            ".g-recaptcha",           # Google reCAPTCHA
            "#captcha",               # Generic CAPTCHA
            "[data-captcha]",         # Data attribute CAPTCHA
            ".h-captcha",             # hCaptcha
            "iframe[src*='captcha']"  # CAPTCHA in iframe
        ]

        for selector in captcha_selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            assert len(elements) == 0, \
                f"CAPTCHA detected with selector '{selector}'. " \
                f"Ethical policy: DO NOT automate forms with CAPTCHAs."
