# -*- coding: utf-8 -*-
"""Web-scraping script that adds abbreviations to abbreviations.txt
   from Oxford English Dictionary website


To Do:
    * Create test script
    * Import required packages into library


Done:

"""

import time
import requests
import urllib.request
from bs4 import BeautifulSoup


def is200(status_code):
    '''Return whether HTTP GET status-code 200 received

    Args:
        status_code (int): Status code as function of GET request
    Return:
        True : status_code == 200
        False: status_code != 200
    '''
    return True if status_code == 200 else False



if __name__ == "__main__":
    # Page where abbreviations will be extracted

    # url_abbrev = "https://public.oed.com/how-to-use-the-oed/abbreviations/#"
    url_abbrev = "http://www.indiana.edu/~letrs/help-services/QuickGuides/oed-abbr.html"

    # Intro
    print("Welcome to abbrescrape!")
    print("This script will update abbreviations.txt with any new " +
          f"abbreviations from '{url_abbrev}'.")

    # Give user choice to quit update: may not be necessary if done recently or
    # if use is unsure whether it is legal to scrape website
    print("***IMPORTANT!!***")
    print("Before scraping any website, verify that it's legal to do so by " +
          "reading its terms of service and/or checking its robots.txt file.")

    ans = input("Would you like to continue (Y/N)? ").strip()

    possible = ['Y', 'y', 'Yes', 'yes',  'N', 'n', 'No', 'no']
    if ans not in possible:
        print("Invalid response. Quitting script.")
        exit()
    if ans in ['N', 'n', 'No', 'no']:
        exit()

    # Fetch web page; check whether successful
    response = requests.get(url_abbrev)
    status_code = response.status_code

    if not is200(status_code):
        print(f"Status code {status_code} unexpected; expecting 200. Quitting "\
              "script.")
        exit()

    print(f"Success: {response}")
