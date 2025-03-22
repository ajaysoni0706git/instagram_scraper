from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import requests
import logging
import os
import re
import emoji

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def dismiss_instagram_popup(driver):
    """
    Detects and dismisses Instagram login popups and modal overlays.
    """
    try:
        logging.info("🔍 Checking for Instagram login popups...")

        # **Method 1**: Click "Not now" button inside the login prompt
        login_popup_xpath = "//div[@role='button' and contains(@class, '_ab8w')]"
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, login_popup_xpath))).click()
        logging.info("✅ Dismissed Instagram login popup.")

    except Exception:
        try:
            # **Method 2**: Click the "Close" button inside the modal overlay
            close_button_xpath = "//div[@role='button' and contains(@class, 'x1i10hfl')]"
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, close_button_xpath))).click()
            logging.info("✅ Dismissed Instagram overlay modal.")
        except Exception:
            logging.info("⚠️ No popups detected.")


def get_postCapImage(post_url):
    """
    Fetches the latest Instagram post's image and caption while handling popups.
    """
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")

    driver = None
    image_path = "latest_instagram_post.jpg"
    caption = "No caption found."

    try:
        driver = uc.Chrome(options=options)
        logging.info(f"🔍 Accessing Instagram post: {post_url}")
        driver.get(post_url)

        # Dismiss login popup if it appears
        dismiss_instagram_popup(driver)

        # Wait for the image to load
        image_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//img[contains(@class, 'x5yr21d')]"))
        )
        image_url = image_element.get_attribute("src")
        logging.info(f"✅ Image URL found: {image_url}")

        # Try to get the caption
        try:
            caption_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(@class, '_ap3a')]"))
            )
            caption = caption_element.text.strip()
            logging.info(f"✅ Caption found: {caption}")
        except Exception:
            logging.warning("⚠️ No caption found.")

        # Download the image
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(image_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            logging.info("✅ Image downloaded successfully.")
        else:
            logging.error(f"❌ Failed to download image. HTTP Status: {response.status_code}")
            image_path = None

    except Exception as e:
        logging.error(f"❌ Error fetching Instagram image/caption: {e}")
        caption, image_path = None, None

    finally:
        if driver:
            driver.quit()

    caption_sorted = clean_caption(caption)

    return caption_sorted

def clean_caption(caption):
    if caption:
        caption = re.sub(r'\s+', ' ', caption).strip() # Remove extra spaces & newlines
        cleaned_caption = emoji.replace_emoji(caption, replace='')  # Remove emojis
        return cleaned_caption
    return "No caption found."
