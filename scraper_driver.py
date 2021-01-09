import sys
from scraper_helper import RedfinScraper

# main
def main():
    try:
        # check arguments
        args = sys.argv[1:]
        args_len = len(args)
        if args_len != 3:
            print("Invalid arguments | Syntax: scraper_driver.py [ChromeDriver path] [location] [size]")
            print("(E.g. %run ./scraper_driver.py \"C:\\Users\\ChromeDriver\\chromedriver.exe\" \"Atlanta, GA\" \"3000\""")")
            sys.exit(0)
        
        # argument variables
        path = args[0]
        loc = args[1]
        size = args[2]
    
        # start data scraper
        print("Starting web scrape task")
        print("Note: If rs_df_tmp.csv is present in directory, it will be imported and possibly overwritten.\n\t- Please remove/rename this file to prevent this from happening.")
        rs = RedfinScraper()
        rs.run(path, loc, int(size))
        
        # gracefully exit
        print("Completed web scrape task")
        sys.exit(0)
    except Exception as e:
        print("Failed to initiate Web scraper: {}".format(str(e)))
        sys.exit(0)
        
if __name__ == "__main__":
    main()
    