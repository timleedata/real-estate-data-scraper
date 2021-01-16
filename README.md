# Real Estate Data Scraper: Overview  
* Built a web scraper for Redfin using Python and Selenium  
* Uses a proxy to avoid IP/port being flagged as a bot  
* Opens the Redfin homepage, searches for the location specified, grabs all the links in the listing cards, and opens each listing to acquire data  
**Note:** This is my first web scraping project and have intentionally left some data messy so to practice cleaning in a different project  

## Requirements  
**Python Version:** 3.8.5  
**Selenium Version:** 3.141.0 ```pip install selenium```  
**ChromeDriver Version:** 87.0.4280.88 - https://sites.google.com/a/chromium.org/chromedriver/downloads  

## Web Scraping  
Scrapes the following details from the listing pages:  
* Address info: street, city, state, zip_code  
* Home info: price, beds, baths, sqft, home_type, sold_history  
* Neighborhood info: neighborhood, walk_score, transit_score, bike_score  

## Instructions  
Run scraper_driver.py:  
* ($python3 ./scraper_driver.py \[ChromeDriver path\] \[location\] \[-s (optional)\] )  
* Using IPython: (%run ./scraper_driver.py \[ChromeDriver path\] \[location\] \[-s (optional)\] )  
* (e.g. %run ./scraper_driver.py "C:\Users\ChromeDriver\chromedriver.exe" "Atlanta, GA" )  
**Note:** For location, "import_loc_file" can be specified to search multiple locations (sample in data/loc_list.csv)  
Also, -s option gets listings that were sold in past 3 months  

Files in data folder:  
* \[from constants.py\] csv_file_name = "rs_df_tmp.csv" -> Temp csv file created after all listing urls are obtained, if file is present, program will use the urls in this file instead of searching Redfin for listings (based on whether url has been checked or not)  
* \[from constants.py\] final_file_name = "rs_df_final.csv" -> Final csv file created after all data obtained  
* \[from constants.py\] loc_file_name = "loc_list.csv" -> File to be used when location is specified as "import_loc_file", should contain the location, city, state info  
