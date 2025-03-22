from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_latest_instagram_post(username):
    # Start Stealth Browser
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")

    driver = None
    post_url = None

    try:
        driver = uc.Chrome(options=options)
        url = f"https://www.instagram.com/{username}/"
        logging.info(f"🔍 Accessing Instagram profile: {url}")
        driver.get(url)

        # Wait for posts to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//article//a")))

        # Find the latest post URL
        latest_post = driver.find_element(By.XPATH, "//article//a")
        post_url = latest_post.get_attribute("href")

        logging.info(f"✅ Latest post URL: {post_url}")

    except Exception as e:
        logging.error(f"❌ Error fetching Instagram post: {e}")

    finally:
        if driver:
            driver.quit()

    return post_url
