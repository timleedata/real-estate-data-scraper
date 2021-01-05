from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
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

    '''
    # enters location into search on homepage
    def _enter_search(self, loc: str) -> bool:
        try:
            search = WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "search-box-input")))
            self._driver.execute_script("arguments[0].value=\"{}\"".format(loc), search)
            button = WebDriverWait(self._driver, 5).until(EC.element_to_be_clickable((By.ID, "search-icon")))
            time.sleep(2)
            self._driver.execute_script("arguments[0].click()", button)
            searched = WebDriverWait(self._driver, 15).until(EC.presence_of_element_located((By.ID, "grid-search-results"))).is_displayed()
            return searched
        except:
            print("Failed to enter search.")
            return False
    '''

    # run
    def run(self, path: str, proxy: str, loc: str) -> bool:
        # set up web driver
        options = webdriver.ChromeOptions()
        options.add_argument('--proxy-server={}'.format(proxy))
        self._driver = webdriver.Chrome(options=options, executable_path=path)
        try:
            search_loc = "https://www.zillow.com/homes/" + loc
            self._driver.get(search_loc)
            if WebDriverWait(self._driver, 15).until(EC.presence_of_element_located((By.ID, "grid-search-results"))).is_displayed():
                self._size += 1 # temporary - should be size of df (max data we want to collect)
                href_list = []
                elements = self._driver.find_elements_by_css_selector(".list-card-info > a")
                for el in elements:
                    href_list.append(el.get_attribute("href"))
                self._driver.get(href_list[0])
                #self._driver.find_element_by_class_name("ds-close-lightbox-icon hc-back-to-list").click()
                return True
            else:
                return False
        except:
            # also catches blocks by captcha
            print("Proxy failed to load page.")
            return False
