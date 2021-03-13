"""
So the goal here would be
- Use selenium to trigger csv downloads from opencritic browsing by date
- For now game that was released at least a week before sysdate (date col)
- It seems the end is 287 pages, but use while statement so when it reaches an empty page, stop the scraping process

"""

# imports
import os,sys
import time
from datetime import datetime,timedelta
import re
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# get logger and utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from logger import logger_data

# get data
from dl_csv import download_csv

# platforms to get
platforms = ['Switch','PS4']

# setting up firefox headless browser
opts = Options()
opts.headless = True
browser = Firefox(options=opts)

# start on page 1
base_url = "https://opencritic.com/browse/all/all-time/date?page=1"
browser.get(base_url)

# get page_num and current page_num
pg_num = 1
while True:
    # close popup for preference settings if it exists
    logger_data.info(f"Scraping page: {pg_num}")
    popups = browser.find_elements_by_xpath("//span[contains(@id,'cmpwelcomebtnno')]")
    if len(popups) != 0:
        popups[0].click()
    time.sleep(1)

    # get games and dates
    game_scores = [i.text for i in browser.find_elements_by_xpath("//div[contains(@class,'score col-auto')]")]
    game_names = [i.text for i in browser.find_elements_by_xpath("//div[contains(@class,'game-name col')]//a")]
    game_links = [i.get_attribute('href') for i in browser.find_elements_by_xpath("//div[contains(@class,'game-name col')]//a")]
    date_results = [i.text for i in browser.find_elements_by_xpath("//div[contains(@class,'first-release-date')]//span")]
    game_platforms = [i.text.split(", ") for i in browser.find_elements_by_xpath("//div[contains(@class,'platforms col-auto')]")]

    logger_data.info(f"{len(game_names)} available, attempt downloading files.")

    # change dates to datetime
    # test: ensure formats are like this
    date_dts = [datetime.strptime(i, '%b %d, %Y') for i in date_results]

    ### if the release date of the game is more than 7days since the sysdate, click and download csv
    # today's date
    dt_now = datetime.now()

    for score,game,link,dt,platform in zip(game_scores,game_names,game_links,date_dts,game_platforms):
        if (dt <= (dt_now - timedelta(days=7))) and (any(x in platforms for x in platform)) and len(score) > 0:
            # download page
            logger_data.info(f"Start scraping {game}")
            download_csv(link,game)

    # add pg_num
    pg_num += 1

    # click to move to next page
    browser.execute_script("arguments[0].click();",
                           WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@rel,'next')]"))))
    time.sleep(3)

    # retrieve next pg_num
    current_pg = browser.find_element_by_xpath("//span[contains(@class,'px-4')]").text
    current_pg = int(re.findall(r'[0-9]+', current_pg)[0])

    # break if intended next pg number is less than actual pg_num
    if current_pg < pg_num:
        logger_data.info("Reached last page, scraping will stop.")
        break

# close browser
browser.close()

