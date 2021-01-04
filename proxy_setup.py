"""
Created on Sun Jan  3 20:17:32 2021

@author: Timothy Lee

"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class ProxyEngine(object):
    
    def __init__(self):
        self._proxy_list = []
        #self._attempts = 10

    def _set_proxies(self, path: str):
        '''
        Below proxy setup logic from DebanjanB: https://stackoverflow.com/a/59410739
        '''
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(chrome_options=options, executable_path=path)
        driver.get("https://sslproxies.org/")
        #driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//th[contains(., 'IP Address')]"))))
        ips = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 1]")))]
        ports = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 2]")))]
        driver.quit()
        for i in range(0, len(ips)):
            self._proxy_list.append(ips[i]+':'+ports[i])
    
    def run(self, path: str) -> str:
        print("Path is: {}.".format(path))
        if not self._proxy_list: # initialize proxy list
            self._set_proxies(path)
        print("Proxy list: {}".format(self._proxy_list))
        '''while self._attempts > 0: # retry after failed attempt
            try:
                proxy = self._proxy_list.pop()
                print("Proxy selected: {}".format(proxy))
                options = webdriver.ChromeOptions()
                options.add_argument('--proxy-server={}'.format(proxy))
                driver = webdriver.Chrome(options=options, executable_path=path)
                #driver.get("https://www.whatismyip.com/proxy-check/?iref=home") - whatismyip.com now blocks potential bots with captcha
                driver.get("https://www.zillow.com/")
                if "Proxy Type" in WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "p.card-text"))):
                    print("Proxy successfully set up.")
                    return proxy
            except Exception:
                print("Error proxy setup.")
                self._attempts -= 1
                print("Number of attempts remaining: {}".format(self._attempts))
                driver.quit()
        '''
        if self._proxy_list:
            return self._proxy_list.pop()
        else:
            print("Error proxy setup.")
            return ""
        