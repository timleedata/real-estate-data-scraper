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
    
    # load df from rs_df_tmp.csv
    def load_csv_file(self) -> bool:
        print("Method: load_csv_file()")
        try:
            self._df = pd.read_csv("rs_df_tmp.csv")
            return True
        except:
            return False

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
        
    '''
    # checks whether current page is captcha
    def check_captcha(self) -> bool:
        print("Method: check_captcha()")
        try:
            WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.ID, "captcha")))
            return True
        except:
            return False
    '''
    
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
        
    # export df to csv for future use
    def export_df_to_csv(self):
        print("Method: export_df_to_csv()")
        try:
            self._df.to_csv("rs_df_tmp.csv")
        except:
            print("Failed to export df to rs_df_tmp.csv")
        
    # create df after listings retrieved
    def create_and_save_df(self) -> bool:
        print("Method: create_and_save_df()")
        try:
            self._df = pd.DataFrame(self._href_list, columns=["url"])
            self._df["Checked"] = 0
            self.export_df_to_csv()
            return True
        except:
            print("Failed to create df")
            return False
    
    # get details from listing cards
    def scrape_listings(self) -> bool:
        print("Method: scrape_listings()")
        try:
            href_list = self._df[self._df['Checked'] == 0]['url'][0:3].tolist()
            print(href_list)
            for url in href_list:
                self._driver.get(url)
                street = WebDriverWait(self._driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[@class='street-address']"))).get_attribute("innerHTML")
                city = WebDriverWait(self._driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[@class='locality']"))).get_attribute("innerHTML")
                state = WebDriverWait(self._driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[@class='region']"))).get_attribute("innerHTML")
                zip_code = WebDriverWait(self._driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[@class='postal-code']"))).get_attribute("innerHTML")
                price = WebDriverWait(self._driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='statsValue']/div/span[2]"))).get_attribute("innerHTML")
                bed = WebDriverWait(self._driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='info-block']/div[@class='statsValue']")))[0].get_attribute("innerHTML")
                bath = WebDriverWait(self._driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='info-block']/div[@class='statsValue']")))[1].get_attribute("innerHTML")
                sqft = WebDriverWait(self._driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='info-block sqft']//span[@class='statsValue']"))).get_attribute("innerHTML")
                home_type = WebDriverWait(self._driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='table-row' and ./span='Style']/div"))).get_attribute("innerHTML")
                neighborhood = WebDriverWait(self._driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h3[@class='h3 walkscore-header']"))).get_attribute("innerHTML")
                walk = WebDriverWait(self._driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='percentage']/span[1]")))[0].get_attribute("innerHTML")
                transit = WebDriverWait(self._driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='percentage']/span[1]")))[1].get_attribute("innerHTML")
                bike = WebDriverWait(self._driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='percentage']/span[1]")))[2].get_attribute("innerHTML")
                
                #sold_prices = [el.get_attribute for el in WebDriverWait(self._driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='sold-row row PropertyHistoryEventRow']//div[@class='price-col number']"))).get_attribute("innerHTML")]
                #sold_dates = [el.get_attribute for el in WebDriverWait(self._driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='sold-row row PropertyHistoryEventRow']/div[@class='col-4']/p[not(@class='subtext')]")))]
                
                print(f"street: {street}\ncity: {city}\nstate: {state}\nzip_code: {zip_code}\nprice: {price}\nbed: {bed}\nbath: {bath}\nsqft: {sqft}\nhome_type: {home_type}\nneighborhood: {neighborhood}\nwalk: {walk}\ntransit: {transit}\nbike: {bike})
                
            return False
        except:
            return True

    # run
    def run(self, path: str, loc: str, size: int):
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
                self.load_csv_file()
                if len(self._df) < size: # only retrieve listings if current df size
                    self._driver.get("https://www.redfin.com/")
                    if self.search_loc(loc):
                        print("Successfully loaded listing page")
                        self._size = size
                        if self.gather_hrefs() and self.create_and_save_df():
                            proxy_failed_or_blocked = self.scrape_listings()
                    else:
                        print("Proxy failed to load page")
                else: # skip getting listings and scan current df
                    proxy_failed_or_blocked = self.scrape_listings()
            except:
                print("Proxy failed to load page")
            
            # close webdriver before looping
            self.close_connection()
        