"""
So the goal here would be
- Use selenium to trigger csv downloads from opencritic browsing by date
- For now game that was released at least a week before sysdate (date col)
- It seems the end is 287 pages, but use while statement so when it reaches an empty page, stop the scraping process

"""

# imports
import os,sys
from datetime import datetime,timedelta
import re
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

# get loogger and utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from logger import logger_data

# get data
import * from dl_csv

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

    # get games and dates
    game_names = [i.text for i in browser.find_elements_by_xpath("//div[contains(@class,'game-name col')]//a")]
    game_links = [i.get_attribute('href') for i in browser.find_elements_by_xpath("//div[contains(@class,'game-name col')]//a")]
    date_results = [i.text for i in browser.find_elements_by_xpath("//div[contains(@class,'first-release-date')]//span")]

    # change dates to datetime
    # test: ensure formats are like this
    date_dts = [datetime.strptime(i, '%b %d, %Y') for i in date_results]

    ### if the release date of the game is more than 7days since the sysdate, click and download csv
    # today's date
    dt_now = datetime.now()

    for game,link,dt in zip(game_names,game_links,date_dts):
        if dt <= (dt_now - timedelta(days=7)):
            # run individual stuff here
            pass

    # add pg_num
    pg_num += 1

    # click to move to next page
    nav = browser.find_elements_by_xpath("//a[contains(@rel,'next')]")
    nav.click()

    # retrieve next pg_num
    current_pg = browser.find_element_by_xpath("//span[contains(@class,'px-4')]").text
    current_pg = int(re.findall(r'[0-9]+', current_pg)[0])

    # break if intended next pg number is less than actual pg_num
    if current_pg < pg_num:
        break

# close browser
browser.close()

