# -*- coding: utf-8 -*-
"""Web-scraping script that adds abbreviations to abbreviations.txt
   from Wiktionary.org


To Do:
    * See whether you can improve collection of abbreviations using filter
      and lambda functions
    * Comment!


Done:
    * Create test script
    * Import required packages into library

"""

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
# ------------------------------------------------------------------------------


# MAIN SCRIPT
# ------------------------------------------------------------------------------

if __name__ == "__main__":

    # First page  where abbreviations will start to be scraped
    mainURL = 'https://en.wiktionary.org'
    startURL = 'https://en.wiktionary.org/w/index.php?title=Category:English_abbreviations&from=A'
    numpages = 21
    delay = 1 # 1 second

    # List to contain fetched abbreviations
    wiki_abbrevs = []

    absURL = startURL

    # Intro
    print("Welcome to abbrevscrape!")
    print("This script will update abbreviations.txt with any new " +
          f"abbreviations from Wikitionary.org.")

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

    for n in range(numpages):
        # Fetch web page; check whether successful
        print(f"Fetching {absURL}...")
        response = requests.get(absURL)
        status_code = response.status_code

        if not is200(status_code):
            print(f"Status code {status_code} unexpected; expecting 200. "\
                  "Quitting script.")
            exit()

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

            # We're only concerned with abbreviations that end with a period
            # Acronyms such as ALCO can be ignored
            if abbrev[-1] == '.':
                # print(abbrev) # DEBUG
                wiki_abbrevs.append(abbrev)



        # Get the hyperlink to next page
        hyperlink = div.find('a', text='next page')
        # print(hyperlink) # DEBUG

        # Get relative URL to next page with abbreviations
        # Caution: program assumes only 21 pages need to be fetched,
        # but this could be changed at any time:
        # If program hits the last page, there will be no next page
        # hyperlink; the following should prevent any unwanted crashes
        if not hyperlink:
            break

        relURL = hyperlink['href']

        # print(relURL) # DEBUG

        absURL =  mainURL + relURL
        # print(absURL) # DEBUG

        time.sleep(delay)


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

# Create sets
wikiset = set(wiki_abbrevs)
userset = set(user_abbrevs)
removeset = set(remove_abbrevs)

# Merge two abbreviations together
abbrevset = wikiset.union(userset)

# Remove any abbreviations that may cause us trouble
abbrevset = wikiset.difference(removeset)

# Sort the set before writing
abbrevset = sorted(abbrevset)

# Write merged and filtered set to abbreviations.txt
with open("abbreviations.txt", 'w') as fout:
    for elem in abbrevset:
        fout.write(elem + '\n')


# DEBUG info
print(wiki_abbrevs) # DEBUG
print(user_abbrevs)
print(remove_abbrevs)
print("*****************")
print(sorted(abbrevset))
print(sorted(wikiset.intersection(userset)))

print(f"# Wikitionary abbreviations = {len(wiki_abbrevs)}")
print(f"# User abbreviations = {len(user_abbrevs)}")
print(f"# Removed abbreviations = {len(remove_abbrevs)}")
print(f"# abbrevs  =  {len(abbrevset)}")
