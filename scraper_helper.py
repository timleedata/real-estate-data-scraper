from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from typing import List
from proxy_setup import ProxyEngine
import pandas as pd

class ZillowScraper(object):
    # init
    def __init__(self):
        self._df = pd.DataFrame()
        self._size = 0
        self._driver = None

    # returns size
    def get_size(self) -> int:
        return self._size

    # returns df
    def get_df(self) -> pd.DataFrame:
        return self._df

    # close current webdriver
    def close_connection(self) -> bool:
        try:
            self._driver.quit()
            return True
        except:
            return False
        
    # checks whether current page is captcha (no current workaround)
    def check_captcha(self) -> bool:
        try:
            WebDriverWait(self._driver, 15).until(EC.presence_of_element_located((By.XPATH, "//meta[@name='robots']"))).is_displayed()
            return True
        except:
            return False
        
    def scrape_listings(self, href_list: List[str]) -> bool:
        for href in href_list:
            self._driver.get(href)
            if self.check_captcha():
                return True
            # else: scraping activity
        return False
    
    # retrieves href links from listing cards (opens in pop up when using webdriver.get())    
    def get_hrefs_by_css(self, css: str) -> List[str]:
        try:
            href_list = []
            elements = self._driver.find_elements_by_css_selector(css)
            for el in elements:
                href_list.append(el.get_attribute("href"))
            return href_list
        except:
            return []

    # run
    def run(self, path: str, loc: str):
        # set up proxy
        proxy_engine = ProxyEngine(path)
    
        # loop - when proxy is blocked (captcha) or failed to load, set new proxy
        proxy_failed_or_blocked = True
        while proxy_failed_or_blocked:
            # set up web driver
            proxy = proxy_engine.set_and_get_proxy()
            options = webdriver.ChromeOptions()
            options.add_argument('--proxy-server={}'.format(proxy))
            self._driver = webdriver.Chrome(options=options, executable_path=path)
            search_loc = "https://www.zillow.com/homes/" + loc
            
            try:
                self._driver.get(search_loc)
                if not self.check_captcha():
                    self._size += 1 # temporary - should be size of df (max data we want to collect)
                    href_list = self.get_hrefs_by_css(".list-card-info > a")
                    proxy_failed_or_blocked = self.scrape_listings(href_list)
            except:
                print("Proxy failed to load page.")
            
            # end loop when desired data size acquired
            proxy_failed_or_blocked = self._size < 5
            
            # close webdriver before looping
            self.close_connection()
        
        
