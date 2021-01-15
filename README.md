# Real Estate Data Scraper (with Python and Selenium)  
Source repo for \[Redfin\] home listings web scraper.  

## Overview
Web scraper for Redfin using Python and Selenium.  
Includes proxy set up which uses a different ip/port each time the proxy is not loading the page or blocked by captcha.  
Process will open the Redfin homepage, use search bar for the location specified, grab all the urls for the listing cards, and open each listing to acquire data.  
Scrapes the following details from the listing pages:  
* Address info: street, city, state, zip_code  
* Home info: price, beds, baths, sqft, home_type, sold_history  
* Neighborhood info: neighborhood, walk_score, transit_score, bike_score  

Files in data/ folder:
* (from constants.py) csv_file_name = "rs_df_tmp.csv" -> Temp csv file created after all listing urls are obtained, if file is present, program will use the urls in this file instead of searching Redfin for listings
* (from constants.py) final_file_name = "rs_df_final.csv" -> Final csv file created after all data obtained
* (from constants.py) loc_file_name = "loc_list.csv" -> File to be used when location is specified as "import_loc_file", should contain the location, city, state info

## Requirements  
Python 3.8.5  
Selenium 3.141.0  
> pip install selenium   

ChromeDriver 87.0.4280.88 (For Google Chrome Version 87.0.4280.88)  
> https://sites.google.com/a/chromium.org/chromedriver/downloads  

## Instructions
Run scraper_driver.py:  
* ($python3 ./scraper_driver.py \[ChromeDriver path\] \[location\] \[-s (optional)\])  
* or IPython (%run ./scraper_driver.py \[ChromeDriver path\] \[location\] \[-s (optional)\])  
**Note:** For location, "import_loc_file" can be used to specify multiple locations (sample in data/loc_list.csv).  
Also, -s option gets listings that were sold in past 3 months.
