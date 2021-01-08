import sys
from scraper_helper import RedfinScraper

# main
def main():
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
    rs = RedfinScraper()
    rs.run(path, loc, size)
    
    # gracefully exit
    print("Completed web scrape task")
    sys.exit(0)
    
if __name__ == "__main__":
    main()
    