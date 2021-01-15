# constants

# proxy set up
proxy_ips = "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 1]" # xpath for ips
proxy_ports = "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 2]" # xpath for port numbers

# scraper general
rf_home_page = "https://www.redfin.com/" # url for redfin home page
first_url = "//div[@class='item-row clickable']/a" # xpath for first url in 'Did you mean?' prompt
filter_btn = "//div[@id='wideSidepaneFilterButtonContainer']/button" # xpath for button to open filters
house_btn = "//div[@id='propertyTypeFilter']//button[1]" # xpath for button to filter listings by houses
condo_btn = "//div[@id='propertyTypeFilter']//button[2]" # xpath for button to filter listings by condos
townhome_btn = "//div[@id='propertyTypeFilter']//button[3]" # xpath for button to filter listings by townhomes
sold_btn = "//div[input[@name='showForSaleToggle']]" # xpath for button to filter listings by sold (in past 3 months)
apply_filter_btn = "//div[@class='applyButtonContainer']/button" # xpath for button to apply filters
listings_check = "//div[@id='right-container']" # xpath for div containing listings to check search success
search_box = "search-box-input" # id for home page search box
captcha_check = "captcha" # id for captcha page check
next_btn = "//button[@class='clickable buttonControl button-text' and @data-rf-test-id='react-data-paginate-next']" # xpath for next button in listings
expand_history_btn =  "//span[@class=' bottomLink font-color-link bottom-link-propertyHistory']" # xpath for expanding listing sold history section
listings_url = "//div[@class='bottomV2']/a" # xpath for url for listings

# scraper listing details
street = "//span[@class='street-address']" # xpath
city = "//span[@class='locality']" # xpath
state = "//span[@class='region']" # xpath
zip_code = "//span[@class='postal-code']" # xpath
price = "//div[@class='statsValue']/div/span[2]" # xpath
price_sold = "//div[@class='info-block price']/div[@class='statsValue']" # xpath
bed_bath = "//div[@class='info-block']/div[@class='statsValue']" # xpath
sqft = "//div[@class='info-block sqft']//span[@class='statsValue']" # xpath
home_type = "//div[@class='table-row' and ./span='Style']/div" # xpath
listing_type = "//span[text()='Listing Type: ']/span" #xpath
neighborhood = "//h3[@class='h3 walkscore-header']" # xpath
scores = "//div[@class='percentage']/span[1]" # xpath
sold_prices = "//div[@class='sold-row row PropertyHistoryEventRow']//div[@class='price-col number']" # xpath
sold_dates = "//div[@class='sold-row row PropertyHistoryEventRow']/div[@class='col-4']/p[not(@class='subtext')]" # xpath

# misc.
csv_file_name = "rs_df_tmp.csv"
final_file_name = "rs_df_final.csv"
loc_file_name = "loc_list.csv"
loc_file_area = "area"
loc_file_city = "city"
loc_file_state = "state"
column_names = ["url", "checked", "street", "city", "state", "zip_code", "price", "beds", "baths", "sqft", "home_type", "neighborhood", "walk_score", "transit_score", "bike_score", "sold_history"]
update_cols_ordered = ["checked", "street", "city", "state", "zip_code", "price", "beds", "baths", "sqft", "home_type", "neighborhood", "walk_score", "transit_score", "bike_score", "sold_history"]