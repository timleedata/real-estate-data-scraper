from proxy_setup import ProxyEngine
from scraper_helper import ZillowScraper

# hardcoded chromedriver path and location to search on Zillow
path = "C:\\{Path to ChromeDriver}\\ChromeDriver\\chromedriver.exe"
loc = "Atlanta, GA"

# initialize proxy and scraper objects
proxy_engine = ProxyEngine()
zs = ZillowScraper()

proxy_failed_or_blocked = True

# loop until desired data size acquired
# resets and attempts new proxy when blocked by captcha or proxy failed to load page
while proxy_failed_or_blocked:
    proxy = proxy_engine.run(path)
    if proxy:
        print("Proxy invoked: {}.".format(proxy))

        processed = zs.run(path, proxy, loc)
        closed = zs.close_connection()
        if processed and closed:
           print("Successfully processed.")
        else: # error processing (failed or blocked proxy) or closing webdriver
            print("Proxy was blocked or failed. Retrying.")
    else: # proxy was not set from proxy engine
        print("Failed to set proxy. Retrying.")
    
    # end loop once desired data size acquired
    if zs.get_size() == 5:
        print("Five successful runs. Completing scrape task.")
        proxy_failed_or_blocked = False
