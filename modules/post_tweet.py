import os
import time
import random
import logging
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def post_tweet(TWITTER_USERNAME, TWITTER_PASSWORD, TWEET_TEXT, IMAGE_PATH):
    
    if not os.path.exists(IMAGE_PATH):
        logging.error("❌ Error: Image file not found!")
        return False

    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = None

    try:
        driver = uc.Chrome(options=options)
        logging.info("🔍 Opening Twitter login page...")
        driver.get("https://twitter.com/login")
        time.sleep(random.uniform(3, 6))

        # Enter username
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )
        type_like_human(driver, username_input, TWITTER_USERNAME)
        username_input.send_keys(Keys.RETURN)
        time.sleep(random.uniform(3, 5))

        # Handle verification step (if required)
        try:
            verify_input = driver.find_element(By.XPATH, '//input[@data-testid="ocfEnterTextTextInput"]')
            logging.warning("🔍 Detected verification step! Entering username again...")
            type_like_human(driver, verify_input, TWITTER_USERNAME)
            verify_input.send_keys(Keys.RETURN)
            time.sleep(random.uniform(3, 5))
        except NoSuchElementException:
            pass

        # Enter password
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        type_like_human(driver, password_input, TWITTER_PASSWORD)
        password_input.send_keys(Keys.RETURN)
        time.sleep(random.uniform(5, 8))

        close_popups(driver)

        # Type tweet
        tweet_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-testid="tweetTextarea_0"]'))
        )
        type_like_human(driver, tweet_box, TWEET_TEXT, delay_range=(0.07, 0.15))
        time.sleep(random.uniform(2, 4))

        # Upload image
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@data-testid="fileInput"]'))
        )
        file_input.send_keys(os.path.abspath(IMAGE_PATH))
        time.sleep(random.uniform(5, 7))

        close_popups(driver)

        # Check if the tweet button is enabled
        for _ in range(10):
            try:
                tweet_button = driver.find_element(By.XPATH, '//button[@data-testid="tweetButtonInline"]')
                if tweet_button.is_enabled():
                    break
            except NoSuchElementException:
                pass
            time.sleep(random.uniform(1, 2))

        # Click tweet button
        tweet_button.click()
        logging.info("✅ Tweet posted successfully with image!")

        return True

    except Exception as e:
        logging.error(f"❌ Error posting tweet: {e}")
        return False

    finally:
        if driver:
            time.sleep(random.uniform(5, 8))
            driver.quit()

def close_popups(driver):
    """
    Closes any popups that appear on Twitter.
    """
    try:
        dismiss_button = driver.find_element(By.XPATH, '//div[@data-testid="confirmationSheetCancel"]')
        dismiss_button.click()
        time.sleep(random.uniform(1, 2))
    except NoSuchElementException:
        pass

def type_like_human(driver, element, text, delay_range=(0.05, 0.2)):
    """
    Types text into an element with random delays to simulate human behavior.
    """
    for index, char in enumerate(text):
        element.send_keys(char)
        time.sleep(random.uniform(*delay_range))

        # Only check for dropdown after the last character
        if index == len(text) - 1:
            try:
                logging.info("🔍 Checking for typeahead results...")

                typeahead_result = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@data-testid='typeaheadResult']"))
                )

                if typeahead_result.is_displayed():
                    logging.info("✅ Typeahead result detected!")

                    # Click outside the dropdown to close it
                    from selenium.webdriver.common.action_chains import ActionChains
                    actions = ActionChains(driver)
                    actions.move_by_offset(10, 10).click().perform()
                    logging.info("📌 Clicked outside to close dropdown.")

            except (TimeoutException, NoSuchElementException):
                logging.info("No typeahead result detected.")
