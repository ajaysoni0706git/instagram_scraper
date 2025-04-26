import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def summarize_with_chatgpt(caption):

    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")

    driver = None
    summary = "No summary generated."

    try:
        driver = uc.Chrome(options=options)
        logging.info("🔍 Opening ChatGPT...")
        driver.get("https://chat.openai.com/")

        # Wait for the input box
        input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "prompt-textarea"))
        )
        input_box.click()
        time.sleep(1)

        # Enter the prompt
        prompt = f"Summarize this into a small tweet with atmost 280 characters without any icons or fonts: {caption}"
        for char in prompt:
            input_box.send_keys(char)
            time.sleep(0.05)  # Simulating human-like typing

        input_box.send_keys(Keys.ENTER)
        logging.info("✅ Prompt submitted to ChatGPT.")

        time.sleep(3)

        # Wait for the response
        response_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.markdown"))
        )
        summary = response_element.text
        print(summary)
        logging.info(f"✅ Summary received: {summary}")

    except Exception as e:
        logging.error(f"❌ Error during ChatGPT summarization: {e}")
        summary = f"Error: {str(e)}"

    finally:
        if summary is not None:
            if driver:
                driver.quit()

    tweet = summary[:280]            
                
    return tweet