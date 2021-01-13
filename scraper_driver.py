from funcs.scraper_helper import RedfinScraper
from funcs.consts.constants import csv_file_name, loc_file_name
import sys

# main
def main():
    try:
        # check arguments
        args = sys.argv[1:]
        args_len = len(args)
        if args_len != 2:
            print("Invalid arguments | Syntax: scraper_driver.py [ChromeDriver path] [location]")
            print("(E.g. %run ./scraper_driver.py \"C:\\Users\\ChromeDriver\\chromedriver.exe\" \"Atlanta, GA\")")
            print(f"Alternatively, specify \"import_loc_file\" as location to use data/{loc_file_name} to search multiple locations")
            sys.exit(0)
        
        # argument variables
        path = args[0]
        loc = args[1]
    
        # start data scraper
        print("Starting web scrape task")
        print(f"Note: If {csv_file_name} is present in data directory, it will be imported and possibly overwritten.\n\t- Please remove/rename this file to prevent this from happening.")
        rs = RedfinScraper()
        rs.run(path, loc)
        
        # gracefully exit
        print("Completed web scrape task")
        sys.exit(0)
    except Exception as e:
        print(f"Failed to initiate Web scraper: {str(e)}")
        sys.exit(0)
        
if __name__ == "__main__":
    main()
    