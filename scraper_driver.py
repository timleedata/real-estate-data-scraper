"""
Created on Sun Jan  3 19:46:17 2021

@author: Timothy Lee
"""

#import pandas as pd
from proxy_setup import ProxyEngine
from scraper_helper import ZillowScraper

path = "C:\\{Path to ChromeDriver}\\ChromeDriver\\chromedriver.exe"

proxy_engine = ProxyEngine()
zs = ZillowScraper()

proxy_failed_or_blocked = True
test_attempts = 10

while proxy_failed_or_blocked:
    proxy = proxy_engine.run(path)
    if proxy:
        print("Proxy invoked: {}.".format(proxy))

        test = zs.run(path, proxy)
        if test:
           # zillow scrape logic here
           print("Works.")
           #proxy_failed_or_blocked = False
        else:
            print("Proxy was blocked or failed. Retrying.")
    else:
        print("Failed to set proxy. Retrying.")
    test_attempts -= 1
    print("Test attempts remaining: {}.".format(test_attempts))
    if test_attempts == 0:
        proxy_failed_or_blocked = False
        