# -*- coding: utf-8 -*-
"""Web-scraping script that retrieves English abbreviations from Wiktionary.org


To Do:
    * Comment!

"""

import sys
import time
import requests
from bs4 import BeautifulSoup


def carry_on(ans):
    '''Determine whether to continue executing script based on user response.
       If the response is either no or something that the code doesn't under-
       stand, the program will exit (with an error code in the former case).

    Args:
        ans (str): User's answer as to whether to carry on with script

    Return:
        Nil
    '''

    # Acceptable answers
    possible = ['Y', 'y', 'Yes', 'yes', 'N', 'n', 'No', 'no']

    if ans not in possible:
        print("Invalid input. Quitting script.", file=sys.stderr)
        sys.exit(2) # UNIX convention for command-line syntax errors
    if ans in ['N', 'n', 'No', 'no']:
        sys.exit()


def scrape_wiki(abs_url, main_url, numpages, delay):
    '''Download all relevant pages from wiktionary.org and parse each page
       for abbreviations

    Args:
        abs_url (str): full URL of page to be downloaded
        main_url (str): Wikitionary's home-page URL
        numpages (int): Number of web pages to be downloaded
        delay (int): time (seconds) program should sleep before downloading
                     next page

     Raise:
        ValueError: Several cases possible
                    i) numpages or delay are negative
                    ii) numpages is zero (scraping doesn't happen)
                    iii) delay is between 0 and 1 seconds (delay too short)

        requests.exceptions.RequestException: in case of connection issues
        reaching URL

    Return:
        wiki_abbrevs (list): abbreviations from downloaded pages
    '''

    if numpages < 0 or delay < 0:
        raise ValueError("numpages or delay cannot be less than zero.")

    if numpages == 0:
        raise ValueError("numpages cannot be 0.")

    if delay < 1:
        raise ValueError("Scrape delay too short; delay must be at least " \
                         "one second.")

    # List to contain fetched abbreviations
    wiki_abbrevs = []

    for _ in range(numpages):
        # Fetch web page; check whether successful
        print(f"Fetching {abs_url}...")

        try:
            response = requests.get(abs_url)

        # No need to catch specific exceptions such as ConnectionError
        # or TimeoutError for this simple script: just catch the basecalsse
        except requests.exceptions.RequestException as err:
            print(f"\nERROR:\n{err}", file=sys.stderr)
            sys.exit("\nCheck that you are connected to the internet " \
                     "and that URL is correct.\n")

        code = response.status_code

        if not is200(code):
            print(f"Status code {code} unexpected: exepecting 200.",
                  file=sys.stderr)
            sys.exit("Quitting script.")

        print(f"{response} => GET successful! Page retrieved.")

        try:
            # Create BS object that will allow you to easily parse the webpage
            soup = BeautifulSoup(response.text, "html.parser")

            # Get section on page that has all the abbreviations
            div = soup.find(id="mw-pages")

            # Zero-in some more to get all the li tags in the div that each contain
            # an abbreviation
            li_tags = div.findAll('li')

            # Each li tag contains a hyperlink. The text of the hyperlink
            # is what we want: an abbreviation
            for li_tag in li_tags:
                wiki_abbrevs.append(li_tag.a.string)

            # Get the hyperlink to next page
            hyperlink = div.find('a', text='next page')

            # Get relative URL to next page with abbreviations
            # Caution: program assumes only 21 pages need to be fetched,
            # but this could be changed at any time:
            # If program hits the last page, there will be no next page
            # hyperlink; the following should prevent any unwanted crashes
            if not hyperlink:
                break

            # Build the URL of the next page to be scraped
            rel_url = hyperlink['href']
            abs_url = main_url + rel_url

        except AttributeError as err:
            # In case we get a page we can scrape but doesn't have the tags
            # we need to process (ie we'll be returned a None somewhere)
            print("AttributeError: {0}".format(err), file=sys.stderr)
            sys.exit()

        # If we scrape site too quickly, it may block us
        time.sleep(delay)

    return wiki_abbrevs


def is200(status_code):
    '''Return whether HTTP GET status-code 200 received

    Args:
        status_code (int): Status code as function of GET request
    Return:
        True : status_code == 200
        False: status_code != 200
    '''
    return status_code == 200


def filter_abbrevs(abbrevs):
    '''Return filtered list of abbreviations from wiktionary

    Args:
        abbrevs (list): Abbreviations from wiktionary

    Return:
        filtered (list): a subset of the list of abbreviations passed by
                         caller
    '''

    # Remove acronyms; only interested in abbreviations that end with a .
    filtered = list(filter(lambda x: x[-1] == '.', abbrevs))
    return filtered


def create_abbrevset(wiki_abbrevs, add_abbrevs, remove_abbrevs):
    '''Return a sorted set of abbreviations that can be written to
       abbreviations.txt and so processed by textanalysis.py.

     Args:
        wiki_abbrevs (list): abbreviations from wiktionary.org
        add_abbrevs (list): user abbreviations from add.txt
        remove_abbrevs(list): user abbreviations from remove.txt

     Return:
        abbrevset (set): sorted set of abbreviations

    '''
    # Sets make it easier to remove duplicates or unwanted elements
    wikiset = set(wiki_abbrevs)
    addset = set(add_abbrevs)
    removeset = set(remove_abbrevs)

    # Merge two abbreviations together
    abbrevset = wikiset.union(addset)

    # Remove any abbreviations that may cause us trouble
    abbrevset = abbrevset.difference(removeset)

    # Sort the set before writing (easier for humans to visually search/debug)
    # Note that an ordered list is returned not a set
    return sorted(abbrevset)


def run():
    '''Execute web-scraping script

    Args:
        nil

    Raise:
        ValueError: if wiki_abbrevs is empty (i.e. nothing scraped!)

    Return:
        nil
    '''

    # First page where abbreviations will start to be scraped
    abs_url = 'https://en.wiktionary.org/w/index.php?title=Category:' \
               'English_abbreviations&from=A'

    main_url = 'https://en.wiktionary.org'

    # Number of abbreviation pages needed for this script
    numpages = 0

    # The delay between fetching each page (in seconds)
    # If we scrape to fast, website might block us.
    delay = 1

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

    # Exit program if user said no or something unintelligible; carry-on if yes
    carry_on(ans)

    # Get all the pages on wiktionary related to abbreviations
    wiki_abbrevs = scrape_wiki(abs_url, main_url, numpages, delay)

    if wiki_abbrevs:
        # Comment out this line if you want to keep acronyms from wiktionary
        wiki_abbrevs = filter_abbrevs(wiki_abbrevs)
    else:
        raise ValueError("List wiki_abbrevs empty.")

    try:
        # Write filtered wiki_abbrevs to file
        with open("wiktionary.txt", 'w') as fout:
            for abbrev in wiki_abbrevs:
                fout.write(abbrev + '\n')

        # Load user-entered abbreviations to be added to abbreviations.txt
        with open("add.txt", 'r') as fin:
            add_abbrevs = fin.read().split('\n')
        # Last item is a blank space; don't need that
        add_abbrevs.pop()

        # Load abbreviations that are too commonly used as nouns or verbs
        # These should not be in the abbreviation list we want for textanalysis
        with open("remove.txt", 'r') as fin:
            remove_abbrevs = fin.read().split('\n')

        # Add and remove any abbreviations from wiktionary
        abbrevset = create_abbrevset(wiki_abbrevs, add_abbrevs, remove_abbrevs)

        # Write final set to abbreviations.txt to be used by textanalysis.py
        with open("abbreviations.txt", 'w') as fout:
            for elem in abbrevset:
                fout.write(elem + '\n')

    except OSError as err:
        # Bad file IO
        print("OS error: {0}".format(err), file=sys.stderr)
        sys.exit()

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        run()
    except ValueError as err:
        print("Value error: {0}".format(err), file=sys.stderr)
