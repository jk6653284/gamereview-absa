"""
So the goal here would be
- Use selenium to trigger csv downloads from opencritic browsing by date
- For now game that was released at least a week before sysdate (date col)
- It seems the end is 287 pages, but use while statement so when it reaches an empty page, stop the scraping process

"""

# imports
from datetime import datetime,timedelta
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

# get data
import * from dl_csv

# setting up firefox headless browser
opts = Options()
opts.headless = True
browser = Firefox(options=opts)

base_url = "https://opencritic.com/browse/all/all-time/date?page={pg_num}"
# while page is still valid
# while pg is valid...think of this logic later

### for the single page, move to the browser and get game and date results
url = base_url.format(pg_num=str(1))
browser.get(url)

# close popup for preference settings if it exists
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

# close browser
browser.close()

