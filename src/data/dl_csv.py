"""
Separate python file for individual page interaction

"""

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

example_url = "https://opencritic.com/game/10642/the-nioh-collection"

class CsvDownloader:
    def __init__(self,url):
        """
        browser: firefox headless browser object
        """
        self.url = url
        self.browser=self.create_browser()

    def create_browser(self):
        opts = Options()
        opts.headless = False
        browser = Firefox(options=opts)
        return browser

    def teardown_browser(self):
        self.browser().close()

    def get_csv_button_link(self):
        # test: ensure num of buttons is 6 (or assert)
        buttons = self.browser.find_elements_by_xpath("//div[contains(@class,'social-buttons')]//a")
        return buttons[-1].get_attribute('href')

    # move to browser by using browser.get(link) from the function above
    def move_to_dl_page(self):
        self.browser.get(self.get_csv_button_link())

    # click on dl link
    def click_and_open_dl_link(self):
        button = self.browser.find_element_by_xpath("//button[contains(@class,'btn btn-block btn-secondary')]")
        button.click()
        # test: ensure new dl link appears
        # assert self.browser.find_element_by_xpath("//a[contains(@class,'btn btn-primary btn-lg')]").text == 'DOWNLOAD CSV'

    def click_on_csv_dl(self):
        button = self.browser.find_element_by_xpath("//a[contains(@class,'btn btn-primary btn-lg')]")
        button.click()
        # test by checking whether or not dl item is in dl folder
        # abspath "/Users/jinibikini/Downloads/" but I can put this in configuration file
        # glob.glob(f"{abspath}*.csv" find all csv files in Downalods folder

        # setting default path here https://stackoverflow.com/questions/60170311/how-to-switch-download-directory-using-selenium-firefox-python


        ### TOOD: bypass dl preference pop-up
    def teardown(self):
        self.browser.close()