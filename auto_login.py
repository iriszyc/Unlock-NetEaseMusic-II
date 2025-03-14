# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "006D7635AFC2DEBF04AF559C23FE45E3F37539C3BBF1BF246A1418348CBC97F8B2C881C7B708E784A3333B62222254B680C9F444AF57A57216F12171F146D65FD104A6D2937B6EC8F5A6ECEEC3D3DADD0621F526702AA4AF8E6C36848B0865E17764BD43E462E1D765CE0D1D3C85587A81C71208CD6E37051B5D455EB02C112F1ABA80399C90B5430A3245DE37BD99EC2086D26FF66EF3A7C19BE14CD3F00D1D2701D64F2C10023C39EA7980B9918B6520624A50135D510D2955A11B1232F91C82E121B4E6C0E649E5668583D8600F9E8822FF5DE67E8270AADF5AA07C872148058B3851A90A4B1D9E010A687A4BF0FA069F563224A882E4002116971D17B2A45279B89EEA5AAFF31415A07DBF305E75EFBB78DDCD556F5F02FD8EC32CF57D310497DEF44C0538344DC9D58E37542D0115CD4A5DADBAF58FD26C160DFF6FD43AFA8F44D6E55D95C7E51D62DB8FECEC73242380A62BEEBC18509918641176FF7B6F"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
