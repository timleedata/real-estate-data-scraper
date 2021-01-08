from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from typing import List, Set
from proxy_setup import ProxyEngine
import pandas as pd

class RedfinScraper(object):
    # init
    def __init__(self):
        self._df = pd.DataFrame()
        self._size = 0
        self._href_list = set()
        self._driver = None

    # returns size
    def get_size(self) -> int:
        return self._size

    # returns df
    def get_df(self) -> pd.DataFrame:
        return self._df

    # retuns href list
    def get_href_list(self) -> Set[str]:
        return self._href_list

    # close current webdriver
    def close_connection(self) -> bool:
        print("Method: close_connection()")
        try:
            self._driver.quit()
            return True
        except:
            print("Failed to close webdriver")
            return False
    
    # click first option in 'Did you mean?'
    def select_first_option(self):
        print("Method: select_first_option()")
        try:
            first_url = WebDriverWait(self._driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='item-row clickable']/a")))[0].get_attribute("href")
            self._driver.get(first_url)
        except:
            print("Failed to select first option ('Did you mean?')")
    
    # default all are checked, this function unchecks apartment, lot/land, and multi-family
    def set_listing_filters(self) -> bool:
        print("Method: set_listing_filters()")
        try:
            # sleeps to avoid bot detection
            WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='wideSidepaneFilterButtonContainer']/button"))).click()
            time.sleep(2)
            WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='propertyTypeFilter']//button[1]"))).click()
            time.sleep(2)
            WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='propertyTypeFilter']//button[2]"))).click()
            time.sleep(2)
            WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='propertyTypeFilter']//button[3]"))).click()
            time.sleep(2)
            WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='applyButtonContainer']/button"))).click()
            return True
        except:
            return False
    
    # checks whether current page is listing page
    def check_listing_page(self) -> bool:
        print("Method: check_listing_page()")
        try:
            WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='HomeViews']")))
            return self.set_listing_filters()
        except:
            return False
    
    # search loc
    def search_loc(self, loc: str) -> bool:
        print("Method: search_loc()")
        try:
            input_box = WebDriverWait(self._driver, 10).until(EC.visibility_of_element_located((By.ID, "search-box-input")))
            input_box.send_keys(loc)
            time.sleep(2) # sleep to avoid bot detection
            input_box.submit()
            self.select_first_option()
            return self.check_listing_page()
        except:
            return False

    # checks whether current page is captcha
    def check_captcha(self) -> bool:
        print("Method: check_captcha()")
        try:
            WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.ID, "captcha")))
            return True
        except:
            return False

    # check if disabled in attributes
    def check_enabled(self, xpath: str)-> bool:
        print("Method: check_enabled()")
        try:
            return WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).is_displayed()
        except:
            return False
    
    # retrieves href links from listing cards
    def gather_hrefs(self) -> bool:
        print("Method: gather_hrefs()")
        try:
            while(len(self._href_list) < self._size):
                hrefs = [el.get_attribute("href") for el in WebDriverWait(self._driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='bottomV2']/a")))]
                href_list = set(hrefs)
                self._href_list |= href_list
                
                next_xpath = "//button[@class='clickable buttonControl button-text' and @data-rf-test-id='react-data-paginate-next']"
                if self.check_enabled(next_xpath):
                    time.sleep(2)
                    self._driver.find_element_by_xpath(next_xpath).click()
                else:
                    self._size = len(self._href_list)
            return True
        except:
            return False
    
    # get details from listing cards
    def scrape_listings(self, href_list: List[str]) -> bool:
        print("Method: scrape_listings()")
        try:
            for href in href_list:
                self._driver.get(href)
                if self.check_captcha():
                    return True
                else:
                    print("Loaded listing card")
                    neighborhood = self._driver.find_element_by_xpath("//div[contains(@class, 'ds-neighborhood')]//h4").get_attribute("innerHTML")
                    walk_transit_scores = [el.get_attribute("innerHTML") for el in self._driver.find_elements_by_xpath("//a[@class='ws-value']//span")]
                    
                    print("Neighborhood: {} | Walk Score: {} | Transit Score: {}".format(neighborhood, walk_transit_scores[0], walk_transit_scores[1]))
            return True
        except:
            return False

    # run
    def run(self, path: str, loc: str, size: str):
        # set up proxy
        proxy_engine = ProxyEngine(path)
    
        # loop - when proxy is blocked (captcha) or failed to load -> set new proxy
        proxy_failed_or_blocked = True
        while proxy_failed_or_blocked:
            # set up web driver
            proxy = proxy_engine.set_and_get_proxy()
            print("Proxy set up complete")
            options = webdriver.ChromeOptions()
            options.add_argument('--proxy-server={}'.format(proxy))
            options.add_argument("--start-maximized")
            self._driver = webdriver.Chrome(options=options, executable_path=path)
            try:
                self._driver.get("https://www.redfin.com/")
                if not self.check_captcha() and self.search_loc(loc):
                    print("Successfully loaded listing page")
                    self._size = int(size)
                    if self.gather_hrefs():
                        proxy_failed_or_blocked = False
                        # temporary test
                        df = pd.DataFrame(self._href_list, columns=['url'])
                        df['Checked'] = 0
                        
                        print("Results:")
                        print(df.head(10))
                        print(df.info())
                        print(len(df))
                else:
                    print("Proxy failed to load page")
            except:
                print("Proxy failed to load page")
            
            # close webdriver before looping
            self.close_connection()
        