#! /usr/bin/env python3
"""
Interface for scraping.py, use this if you want to run any scraping.py methods from the command line.
"""

import os
import sys


if __name__ == '__main__':
    # Make the project root an import path directory:
    sys.path.append(os.getcwd())
    from lib.scraping import GamesJobDirectScraper, GameindustryBizScraper
    for scraper_class in (GamesJobDirectScraper, GameindustryBizScraper):
        scraper_class().main()
