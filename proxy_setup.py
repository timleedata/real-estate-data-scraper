from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from typing import List

class ProxyEngine(object):
    # init
    def __init__(self, path: str = ""):
        self._proxy_list = []
        self._curr_proxy = ""
        self._path = path
        
    # gets proxy list
    def get_proxy_list(self) -> List[str]:
        return self._proxy_list
    
    # returns current proxy
    def get_proxy(self) -> str:
        return self._curr_proxy
    
    # gets proxies from sslproxies.org - ips are rotated every minute
    def _set_proxy_list(self):
        # set up webdriver
        '''
        Below proxy setup logic from DebanjanB: https://stackoverflow.com/a/59410739
        '''
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=options, executable_path=self._path)
        
        # get proxies and append to list
        driver.get("https://sslproxies.org/")
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//option[@value='US']"))).click()
        ips = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 1]")))]
        ports = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 2]")))]
        driver.quit()
        for i in range(0, len(ips)):
            self._proxy_list.append(ips[i]+':'+ports[i])
        
    # gets proxy, if proxy list is empty then retrive proxies
    def set_and_get_proxy(self) -> str:
        # set new proxy list if empty
        if not self._proxy_list:
            self._set_proxy_list()
        
        # set new curr proxy
        self._curr_proxy = self._proxy_list.pop()
        
        return self._curr_proxy
