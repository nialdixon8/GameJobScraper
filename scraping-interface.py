#! /usr/bin/env python3
"""
Interface for scraping.py, use this if you want to run any scraping.py methods from the command line.
"""

import os
import sys
import time
from datetime import datetime as dt

if __name__ == '__main__':
    # Make the project root an import path directory:
    sys.path.append(os.getcwd())
    from lib.scraping import GamesJobDirectScraper, GameindustryBizScraper, AardvarkSwiftScraper, AmiqusScraper
    timestamp = dt.now()
    start_all = time.time()
    # for scraper_class in (GamesJobDirectScraper, GameindustryBizScraper, AardvarkSwiftScraper, AmiqusScraper):
    for scraper_class in (GamesJobDirectScraper, AmiqusScraper):
        start = time.time()
        scraper_class(timestamp).main()
        end = time.time()
        print('{} done in {:.2f}s'.format(scraper_class.__name__, end - start))
    end_all = time.time()
    print('Total scraping time: {:.2f}s'.format(end_all - start_all))
