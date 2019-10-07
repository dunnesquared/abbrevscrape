# -*- coding: utf-8 -*-
"""Web-scraping script that adds abbreviations to abbreviations.txt
   from Wiktionary.org


To Do:
    * Comment!


Done:
    * Create test script
    * Import required packages into library
    * See whether you can improve collection of abbreviations using filter
      and lambda functions

"""

import sys
import time
import requests
import urllib.request
from bs4 import BeautifulSoup

# HELPER FUNCTIONS
# ------------------------------------------------------------------------------
def is200(status_code):
    '''Return whether HTTP GET status-code 200 received

    Args:
        status_code (int): Status code as function of GET request
    Return:
        True : status_code == 200
        False: status_code != 200
    '''
    return True if status_code == 200 else False


def filter_abbrevs(abbrevs):
    '''Return filtered list of abbreviations

    Args:
        abbrevs (list): Abbreviations from wikitionary

    Return:
        filtered (list): a subset of the list of abbreviations passed by
                         caller
    '''

    # Remove acronyms; only interested in abbreviations that end with a .
    filtered = list(filter(lambda x: x[-1] == '.', abbrevs))

    return filtered

# ------------------------------------------------------------------------------


# MAIN SCRIPT
# ------------------------------------------------------------------------------

if __name__ == "__main__":


    # First page where abbreviations will start to be scraped
    startURL = 'https://en.wiktionary.org/w/index.php?title=Category:' \
               'English_abbreviations&from=A'

    mainURL = 'https://en.wiktionary.org'

    # Number of abbreviation pages needed for this script
    numpages = 21

    # The delay between fetching each page (in seconds)
    # If we scrape to fast, website might block us.
    delay = 1

    # List to contain fetched abbreviations
    wiki_abbrevs = []

    absURL = startURL

    # Intro
    print("Welcome to abbrevscrape!")
    print("This script will update abbreviations.txt with any new " +
          "abbreviations from Wikitionary.org.")

    # Give user choice to quit update: may not be necessary if done recently or
    # if use is unsure whether it is legal to scrape website
    print("***IMPORTANT!!***")
    print("Before scraping any website, verify that it's legal to do so by " +
          "reading its terms of service and/or checking its robots.txt file.")
    ans = input("Would you like to continue (Y/N)? ").strip()
    possible = ['Y', 'y', 'Yes', 'yes', 'N', 'n', 'No', 'no']

    if ans not in possible:
        print("Invalid input. Quitting script.", file=sys.stderr)
        sys.exit(2) # UNIX convention for command-line syntax errors
    if ans in ['N', 'n', 'No', 'no']:
        sys.exit()

    for n in range(numpages):
        # Fetch web page; check whether successful
        print(f"Fetching {absURL}...")

        try:
            response = requests.get(absURL)

        # No need to catch specific exceptions such as ConnectionError
        # or TimeoutError for this simple script: just catch the basecalsse
        except requests.exceptions.RequestException as e:
            print(f"\nERROR:\n{e}", file=sys.stderr)
            sys.exit("\nCheck that you are connected to the internet " \
                     "and that URL is correct.\n")

        status_code = response.status_code

        if not is200(status_code):
            print(f"Status code {status_code} unexpected: exepecting 200.",
                  file=sys.stderr)
            sys.exit("Quitting script.")

        print(f"{response} => GET successful! Page retrieved.")

        # Create BS object that will allow you to easily parse the webpage
        soup = BeautifulSoup(response.text, "html.parser")

        # Get section on page that has all the abbreviations
        div = soup.find(id="mw-pages")

        # Zero-in some more to get all the li tags in the div that each contain
        # an abbreviation
        li_tags = div.findAll('li')

        # Each li tag contains a hyperlink. The text of the hyperlink
        # is what we want
        for li_tag in li_tags:
            # Feteched abbreviation!
            abbrev = li_tag.a.string

            wiki_abbrevs.append(abbrev)

        # Get the hyperlink to next page
        hyperlink = div.find('a', text='next page')

        # Get relative URL to next page with abbreviations
        # Caution: program assumes only 21 pages need to be fetched,
        # but this could be changed at any time:
        # If program hits the last page, there will be no next page
        # hyperlink; the following should prevent any unwanted crashes
        if not hyperlink:
            break

        relURL = hyperlink['href']
        absURL =  mainURL + relURL

        time.sleep(delay)


# Comment out this line if you want to keep everything from wikitionary
wiki_abbrevs = filter_abbrevs(wiki_abbrevs)

# Write abbreviations to file
with open("wikitionary.txt", 'w') as fout:
    for abbrev in wiki_abbrevs:
        fout.write(abbrev + '\n')

# Load user-entered abbreviations
with open("user.txt", 'r') as fin:
    user_abbrevs = fin.read().split('\n')

# Last item is a blank space; don't need that
user_abbrevs.pop()

# Load abbreviations that are too commonly used as nouns or verbs
# These should not be in the abbreviation list we want for textanalysis
with open("remove.txt", 'r') as fin:
    remove_abbrevs = fin.read().split('\n')

# Sets make it easier to remove duplicates or unwanted elements
wikiset = set(wiki_abbrevs)
userset = set(user_abbrevs)
removeset = set(remove_abbrevs)

# Merge two abbreviations together
abbrevset = wikiset.union(userset)

# Remove any abbreviations that may cause us trouble
abbrevset = abbrevset.difference(removeset)

# Sort the set before writing (easier for humans to visually search/debug)
abbrevset = sorted(abbrevset)

# Write merged and filtered set to abbreviations.txt
with open("abbreviations.txt", 'w') as fout:
    for elem in abbrevset:
        fout.write(elem + '\n')
