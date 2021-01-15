from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import List, Set
from funcs.proxy_setup import ProxyEngine
from funcs.consts import constants
import time
import pandas as pd

class RedfinScraper(object):
    # init
    def __init__(self):
        self._df = pd.DataFrame() # main df
        self._href_set = set() # urls for listings
        self._href_list = []
        self._driver = None # webdriver
        self._sold = False
        self._loc_list = []
        self._change_proxy = True
        self._added_count = 0

    # returns df
    def get_df(self) -> pd.DataFrame:
        return self._df

    # retuns href list
    def get_href_list(self) -> Set[str]:
        return self._href_list
    
    # returns loc list
    def get_loc_list(self) -> List[str]:
        return self._loc_list
    
    # returns first item from loc list
    def get_first_loc(self, loc_list: List[str]) -> str:
        if loc_list:
            return loc_list[0]
        else:
            return ""
    
    # load loc from location list csv file
    def load_loc_file(self):
        print("Method: load_loc_file()")
        try:
            df = pd.read_csv(f"data/{constants.loc_file_name}", dtype="string") # csv file to specify list of locations
            df["search"] = df[constants.loc_file_area] + ", " + df[constants.loc_file_city] + ", " + df[constants.loc_file_state]
            self._loc_list = df["search"].tolist()
            return True
        except:
            return False
    
    # load df from temp df csv file
    def load_csv_file(self) -> bool:
        print("Method: load_csv_file()")
        try:
            df = pd.read_csv(f"data/{constants.csv_file_name}", dtype="string") # temp csv file to hold progress in case of failure
            if set(constants.column_names).issubset(set(df.columns)):
                self._df = df
                return True
            else:
                print(f"Columns from {constants.csv_file_name} not matching, creating new .csv file (original will be overwritten)")
                return False
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
    def select_first_option(self) -> bool:
        print("Method: select_first_option()")
        try:
            first_url = WebDriverWait(self._driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, constants.first_url)))[0].get_attribute("href")
            self._driver.get(first_url)
            return True
        except:
            return False
    
    # sets filter for listings sold in past 3 months
    def set_recently_sold(self) -> bool:
        print("Method: set_recently_sold()")
        try:
            WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable((By.XPATH, constants.filter_btn))).click() # filter button
            time.sleep(2)
            WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable((By.XPATH, constants.sold_btn))).click() # sold button
            time.sleep(2)
            WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable((By.XPATH, constants.apply_filter_btn))).click() # apply button
            return True
        except:
            return False
            
    '''
    # sets filters for listings as houses (single-faily), condo, townhomes
    def set_listing_filters(self) -> bool:
        print("Method: set_listing_filters()")
        try:
            # sleeps to avoid bot detection
            WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable((By.XPATH, constants.filter_btn))).click() # filter button
            time.sleep(2)
            WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable((By.XPATH, constants.house_btn))).click() # houses button
            time.sleep(2)
            WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable((By.XPATH, constants.condo_btn))).click() # condos button
            time.sleep(2)
            WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable((By.XPATH, constants.townhome_btn))).click() # townhomes button
            time.sleep(2)
            WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable((By.XPATH, constants.apply_filter_btn))).click() # apply button
            return True
        except:
            return False
    '''
    
    # checks whether current page is listing page
    def check_listing_page(self) -> bool:
        print("Method: check_listing_page()")
        try:
            WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.XPATH, constants.listings_check))) # div for listings
            #return self.set_listing_filters()
            if self._sold:
                return self.set_recently_sold()
            else:
                return True
        except:
            return False
    
    # search loc
    def search_loc(self, loc: str) -> bool:
        print("Method: search_loc()")
        try:
            input_box = WebDriverWait(self._driver, 10).until(EC.visibility_of_element_located((By.ID, constants.search_box))) # search box in home page
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
            WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.ID, constants.captcha_check)))
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
            next_enabled = True
            while(next_enabled):
                hrefs = [el.get_attribute("href") for el in WebDriverWait(self._driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, constants.listings_url)))]
                href_set = set(hrefs)
                self._href_set |= href_set
                
                if self.check_enabled(constants.next_btn):
                    time.sleep(2)
                    self._driver.find_element_by_xpath(constants.next_btn).click()
                else:
                    next_enabled = False
            return True
        except:
            return False
        
    # export df to csv for future use
    def export_df_to_csv(self, file_name: str):
        print("Method: export_df_to_csv()")
        try:
            self._df.to_csv(f"data/{file_name}", index=False)
        except:
            print(f"Failed to export df to {file_name}")
        
    # convert href set to list for df create
    def convert_href(self) -> bool:
        try:
            self._href_list = [{"url":href} for href in self._href_set]
            return True
        except:
            print("Failed to convert href set to List[dict]")
            return False
        
    # create df after listings retrieved
    def create_and_save_df(self) -> bool:
        print("Method: create_and_save_df()")
        try:
            if self.convert_href(): # formatting for column and df creation
                self._df = pd.DataFrame(data=self._href_list, columns=constants.column_names, dtype="string")
                self._df["checked"] = 0
                self.export_df_to_csv(constants.csv_file_name)
                return True
            else:
                return False
        except:
            print("Failed to create df")
            return False
    
    # tries to get element, returns blank if not found
    def blank_or_element_xpath(self, xpath: str) -> str:
        try:
            el = WebDriverWait(self._driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath))).get_attribute("innerHTML")
            return el
        except:
            return ""
    
    # tries to get all elements, returns blank if not found
    def blank_or_all_elements_xpath(self, xpath: str) -> List[str]:
        try:
            el_list = [el.get_attribute("innerHTML") for el in WebDriverWait(self._driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, xpath)))]
            return el_list
        except:
            return []
    
    # click expand if exists
    def click_history_expand(self) -> bool:
        try:
            WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable((By.XPATH, constants.expand_history_btn))).click()
            return True
        except:
            return False
        
    # tries to get sold history, returns blank if not found
    def blank_or_sold_history(self) -> str:
        try:
            self.click_history_expand()
            sold_history = ""
            sold_prices = [el.get_attribute("innerHTML") for el in WebDriverWait(self._driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, constants.sold_prices)))]
            sold_dates = [el.get_attribute("innerHTML") for el in WebDriverWait(self._driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, constants.sold_dates)))]
            for i in range(len(sold_prices)):
                sold_history += sold_prices[i] + ":" + sold_dates[i] + ";"
            return sold_history[:-1]
        except:
            return ""
    
    # get details from listing cards
    def scrape_listings(self) -> bool:
        print("Method: scrape_listings()")
        try:
            href_list = self._df[self._df["checked"] == 0]["url"].tolist()
            while href_list:
                url = self.get_first_loc(href_list)
                self._driver.get(url)
                
                # test page loaded
                street = WebDriverWait(self._driver, 10).until(EC.visibility_of_element_located((By.XPATH, constants.street))).get_attribute("innerHTML")
                
                # listing details
                city = self.blank_or_element_xpath(constants.city)
                state = self.blank_or_element_xpath(constants.state)
                zip_code = self.blank_or_element_xpath(constants.zip_code)
                price = self.blank_or_element_xpath(constants.price_sold) if self._sold else self.blank_or_element_xpath(constants.price)
                bed_bath = self.blank_or_all_elements_xpath(constants.bed_bath)
                bed_bath_cond = len(bed_bath) >= 2
                beds = bed_bath[0] if bed_bath_cond else ""
                baths = bed_bath[1] if bed_bath_cond else ""
                sqft = self.blank_or_element_xpath(constants.sqft)
                home_type = self.blank_or_element_xpath(constants.home_type)
                home_type = home_type if home_type else self.blank_or_element_xpath(constants.listing_type)
                neighborhood = self.blank_or_element_xpath(constants.neighborhood)
                scores = self.blank_or_all_elements_xpath(constants.scores)
                scores_cond = len(scores) >= 3
                walk_score = scores[0] if scores_cond else ""
                transit_score = scores[1] if scores_cond else ""
                bike_score = scores[2] if scores_cond else ""
                sold_history = self.blank_or_sold_history()
                
                # update values in row based on url
                self._df.loc[self._df["url"]==url, constants.update_cols_ordered] = [1, street, city, state, zip_code, price, beds, baths, sqft, home_type, neighborhood, walk_score, transit_score, bike_score, sold_history]
                href_list.pop(0)
                self._added_count += 1
                print(f"Current count: {self._added_count}")
            return True
        except:
            return False

    # run
    def run(self, path: str, loc: str, sold: bool):
        # read in .csv file (if any)
        is_df_loaded = self.load_csv_file()
        
        # set loc list
        if loc == "import_loc_file":
            self.load_loc_file()
        else:
            self._loc_list.append(loc)
            
        self._sold = sold
            
        # set up proxy
        proxy_engine = ProxyEngine(path)
    
        # loop - when proxy is blocked (captcha) or failed to load -> set new proxy
        proxy_failed_or_blocked = True
        while proxy_failed_or_blocked:
            if self._change_proxy:
                # set up web driver
                proxy = proxy_engine.set_and_get_proxy()
                options = webdriver.ChromeOptions()
                options.add_argument(f"--proxy-server={proxy}")
                options.add_argument("--start-maximized")
                self._driver = webdriver.Chrome(options=options, executable_path=path)
                print("Proxy set up complete")

            try:
                if is_df_loaded: # skip getting listings and scan current df
                    if self.scrape_listings():
                        proxy_failed_or_blocked = False
                        print("Successfully scraped and updated df with listing details")
                        self.export_df_to_csv(constants.final_file_name)
                    else:
                        self._change_proxy = True
                elif self._loc_list:
                    loc = self.get_first_loc(self._loc_list)
                    self._driver.get(constants.rf_home_page)
                    if self.search_loc(loc) and self.gather_hrefs():
                        print("Successfully added listing urls")
                        self._loc_list.pop(0)
                        self._change_proxy = False
                    else:
                        print("Proxy failed to load listing page")
                        self._change_proxy = True
                elif self.create_and_save_df():
                    is_df_loaded = True
                else: # ideally should not reach -> exit if error saving .csv file
                    print("Failed to get listings and save to .csv file, exiting")
                    proxy_failed_or_blocked = False
            except:
                self._change_proxy = True
                print("Proxy failed to load page")
            
            if self._change_proxy or not proxy_failed_or_blocked:
                # close webdriver before looping
                self.close_connection()
        