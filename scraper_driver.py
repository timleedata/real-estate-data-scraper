import sys
from scraper_helper import ZillowScraper

# main
def main():
    # check arguments
    args = sys.argv[1:]
    args_len = len(args)
    if args_len != 2:
        print("Invalid arguments. Syntax: scraper_driver.py [ChromeDriver path] [city] [state]")
        print("(E.g. %run ./scraper_driver.py \"C:\\Users\\ChromeDriver\\chromedriver.exe\" \"Atlanta GA\")")
        sys.exit(0)
    
    # argument variables
    path = args[0]
    loc = args[1]

    # start data scraper
    print("Starting web scrape task.")
    zs = ZillowScraper()
    zs.run(path, loc)
    
    # gracefully exit
    print("Completed web scrape task.")
    sys.exit(0)
    
if __name__ == "__main__":
    main()
    