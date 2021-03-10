"""
Separate python file for individual page interaction

"""
import os, sys
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException,TimeoutException
import time

# get logger and utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from logger import logger_data


dl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "csvs/")

def download_csv(url, game_title):
    opts = Options()
    opts.headless = True

    # set preferences
    profile = FirefoxProfile()
    profile.set_preference("browser.download.panel.shown", False)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", 'text/csv')
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.dir", dl_path)
    browser = Firefox(options=opts, firefox_profile=profile)

    # get browser
    browser.get(url)
    popup = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(@id,'cmpwelcomebtnno')]"))
    )
    popup.click()
    logger_data.debug("Closed popup.")

    # get download link
    try:
        buttons = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class,'social-buttons')]//a"))
        )

        csv_link = buttons[-1].get_attribute('href')
        browser.get(csv_link)
        logger_data.debug(f"Moved to csv link page for {game_title}.")
    except Exception:
        logger_data.error(f"Can't get csv link. Moving on to next download.",
                          exc_info=True)
        browser.close()

    # so for some reason this was causing all the problem.
    # browser needed time to load while moving to another link.
    # but I'm pretty sure this is the purpose of WebDriverWait class????
    # need to know why forced time wait works and the other doesn't
    time.sleep(3)
    try:
        button = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'btn btn-block btn-secondary')]"))
        )
        button.click()
        logger_data.debug(f"Opened csv download link for {game_title}.")

        button = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class,'btn btn-primary btn-lg')]"))
        )

        button.click()
        logger_data.info(f"Download successful for {game_title}.")
    except StaleElementReferenceException:
        logger_data.error("Unable to locate button for download. Moving on to next download.",
                          exc_info=True)
    except TimeoutException:
        logger_data.error("Timeout. Moving on to next download.",
                          exc_info=True)

    browser.close()
