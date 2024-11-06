import os
import time
import logging
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import traceback


# Load environment variables
load_dotenv()
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
qty = os.getenv('QTY', 2)
phone = os.getenv('PHONE')
username = os.getenv('USERNAME')

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

logger.info("Script started")

try:
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')

    # Initialize the Chrome driver using webdriver-manager
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    driver.maximize_window()
    driver.get("https://rush.telecharge.com/")
    logger.info("Navigated to the website")

    # Locate and switch to the iframe
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
    )
    driver.switch_to.frame(iframe)
    logger.info("Switched to iframe")

    # Locate and click the sign-in button
    sign_in_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "st_sign_in"))
    )
    sign_in_button.click()
    logger.info("Clicked on sign-in button")

    # Locate and click the LinkedIn button
    linkedin = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "st_campaign_social_media_button_long_linkedin"))
    )
    linkedin.click()
    logger.info("Clicked on LinkedIn logo image")

    # Handle the new window
    original_window = driver.current_window_handle
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            logger.info("Switched to LinkedIn window")
            break

    # Enter username and password
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    username_field.send_keys(username)
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)

    # Click the LinkedIn "Sign In" button
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn__primary--large"))
    )
    login_button.click()
    logger.info("Clicked LinkedIn sign-in button")

    # Handle LinkedIn allow button
    try:
        allow_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "actions__allow"))
        )
        allow_button.click()
        logger.info("Clicked allow button")
    except Exception:
        logger.warning("Allow button did not appear; proceeding without clicking it")

    # Return to the original window
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(1))
    driver.switch_to.window(original_window)
    logger.info("Returned to the original window")

    # Locate and switch to the iframe again
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
    )
    driver.switch_to.frame(iframe)
    logger.info("Switched to iframe again")

    # Locate the lottery entry button
    enter_lott = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "st_campaign_nav_item_id_3551"))
    )
    enter_lott.click()
    logger.info("Clicked to enter lottery")

    # Click the lottery entry buttons
    buttons = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.st_campaign_button.st_style_button.st_uppercase"))
    )
    logger.info(f"Found {len(buttons)} lottery buttons to click")

    # Enter contact information
    email_field = driver.find_element(By.ID, "email")
    email_field.clear()
    email_field.send_keys(email)
    logger.info("Entered email")
    if phone:
        phone_field = driver.find_element(By.ID, "phone_number")
        phone_field.clear()
        phone_field.send_keys(phone)
        logger.info("Entered phone number")

    dropdowns = driver.find_elements(By.XPATH, "//select[starts-with(@id, 'tickets_')]")
    logger.info(f"Found {len(dropdowns)} dropdowns")

    for index, button in enumerate(buttons):
        driver.execute_script("arguments[0].scrollIntoView(true);", dropdowns[index])
        dropdown = Select(dropdowns[index])
        dropdown.select_by_value(qty)
        time.sleep(0.5)
        button.click()
        logger.info(f"Clicked button {index + 1}/{len(buttons)}")
        time.sleep(2)

    logger.info("Script completed successfully")

except Exception as e:
    logger.error(f"An error occurred: {e}")
    traceback.print_exc()
