# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 00:42:25 2021

@author: seyun
"""

from selenium import webdriver
import pandas as pd
import time

class ZillowScraper(object):
    
    def __init__(self):
        self._df = pd.DataFrame()
        
    def run(self, path: str, proxy: str) -> bool:
        options = webdriver.ChromeOptions()
        options.add_argument('--proxy-server={}'.format(proxy))
        driver = webdriver.Chrome(options=options, executable_path=path)
        try:
            driver.get("https://www.zillow.com/")
            time.sleep(5)
            if driver.find_element_by_id("search-icon").is_displayed():
                driver.quit()
                return True
            else:
                print("Could not load home page.")
                driver.quit()
                return False
        except:
            driver.quit()
            print("Proxy failed.")
            return False