# -*- coding: utf-8 -*-

"""Wiktionary Abbreviation Scraper

The purpose of this script is to create a text file containing a list of
abbreviations commonly used in English. The intended user of this list is
module "textanalysis", which uses the abbreviation file to help extract
sentences from a a text.

Abbreviations are scraped from Wiktionary.org. Continuous thanks to the
many Wikimedia contributors who make it possible to write scripts like
these!

The main output file of this script is "abbreviations.txt". This is the file
the textanalysis module uses. The other output file is "wiktionary.txt",
which is a superset of "abbreviations.txt".

In this script, an abbreviation is any one-word, alphanumeric string (under-
scores allowed) that ends with a period. Acronyms and multi-word abbreviations
are thus filtered out.

Pleae read "readme.txt" before writing abbreviations to "add.txt" or
"remove.txt". Incorrect updates to these files will lead to unexpected results.

This script requires 'requests' and 'BeautifulSoup' be installed in the Python
environment where this script runs. This script should be compatible with
Python 3.6.1 or above.

No command-line parameters are required to run this script–only an internet
connection and permission to write to the abbrevscrape folder.

This file can also be imported as a module and contains the following
public functions:

    * scrape_wiki - returns a 'list' object containing Wiktionary abbreviations

    * filter_abbrevs - returns a filtered list of the above

    * create_abbrevlist - returns a sorted 'list' obj filtering out abbrevia-
                          tions from 'remove.txt' but adding ones from
                          'add.txt'.

    * run - the main body of the script
"""

import sys
import time
import re
import requests
from bs4 import BeautifulSoup


def _carry_on(ans):
    """Determines whether to continue executing script based on user response.

    If the response is either 'No' or something that the code doesn't under-
    stand, the program will exit (with an error code in the former case).

    Args:
        ans (str): User's answer as to whether to carry on with script
    """

    # Acceptable answers
    possible = ['Y', 'y', 'Yes', 'yes', 'N', 'n', 'No', 'no']

    if ans not in possible:
        print("Invalid input. Quitting script.", file=sys.stderr)
        sys.exit(2) # UNIX convention for command-line syntax errors

    if ans in ['N', 'n', 'No', 'no']:
        sys.exit()


def scrape_wiki(abs_url, main_url, numpages, delay):
    """Downloads Wiktionary abbreviation pages and parses each page

    Args:
        abs_url (str): full URL of page to be downloaded
        main_url (str): Wiktionary's home-page URL
        numpages (int): Number of web pages to be downloaded
        delay (int): time (seconds) program should sleep before downloading
                     next page

    Returns:
        wiki_abbrevs (list): string abbreviations from downloaded pages

    Raises:
       ValueError: Several cases possible
                   i) numpages or delay are negative
                   ii) numpages is zero (scraping doesn't happen)
                   iii) delay is between 0 and 1 seconds (delay too short)

       requests.exceptions.RequestException: in case of connection issues
                                             reaching URL
    """

    if numpages < 0 or delay < 0:
        raise ValueError("numpages or delay cannot be less than zero.")

    if numpages == 0:
        raise ValueError("numpages cannot be 0.")

    # Too short of a delay may cause website to block us
    if delay < 1:
        raise ValueError("Scrape delay too short; delay must be at least " \
                         "one second.")

    # List to contain abbreviations parsed from downloaded pages
    wiki_abbrevs = []

    for _ in range(numpages):

        # Fetch web page; check whether successful
        print(f"Fetching {abs_url}...")

        try:
            response = requests.get(abs_url)

        # No need to catch specific exceptions such as ConnectionError
        # or TimeoutError for this simple script: just catch the base class
        except requests.exceptions.RequestException as err:
            print(f"\nERROR:\n{err}", file=sys.stderr)
            sys.exit("\nCheck that you are connected to the internet " \
                     "and that URL is correct.\n")

        # See whether we retrieved the page successfully or not
        stat_code = response.status_code

        if not _is200(stat_code):
            print(f"Status code {stat_code} unexpected: exepecting 200.",
                  file=sys.stderr)
            sys.exit("Quitting script.")

        print(f"{response} => GET successful! Page retrieved.")

        try:

            print("Parsing page for abbreviations...", end="")

            # Create BS object that will allow you to easily parse the webpage
            soup = BeautifulSoup(response.text, "html.parser")

            # Get section on page that has all the abbreviations
            div = soup.find(id="mw-pages")

            # Zero-in some more to get all the li tags in the div. Each li
            # contains a hperlink which in turns contains an abbreviation
            li_tags = div.findAll('li')

            # Collect the text from each hyperlink, i.e. the abbreviation
            for li_tag in li_tags:
                wiki_abbrevs.append(li_tag.a.string)

            # Get the hyperlink to the next page we want to download
            hyperlink = div.find('a', text='next page')

            # Get relative URL to the next page with abbreviations
            # Caution: program assumes only 21 pages need to be fetched,
            # but this could be changed at any time:
            # If program hits the last page, there will be no next page
            # hyperlink; the following should prevent any unwanted crashes
            # in such a case.
            if not hyperlink:
                break

            # Build the URL of the next page to be scraped
            rel_url = hyperlink['href']
            abs_url = main_url + rel_url

            # If we scrape site too quickly, it may block us
            time.sleep(delay)

            print("DONE!")

        except AttributeError as err:

            # In case we get a page we can scrape but doesn't have the tags
            # we need to process (ie we'll be returned a None somewhere)
            print("AttributeError: {0}".format(err), file=sys.stderr)
            sys.exit()

    return wiki_abbrevs


def _is200(status_code):
    """Returns whether HTTP GET status-code 200 received

    Args:
        status_code (int): Status code as function of GET request

    Returns:
        True : status_code == 200
        False: status_code != 200
    """

    return status_code == 200


def filter_abbrevs(abbrevs):
    """Removes abbreviations that are more than one word or don't end with '.'

    Args:
        abbrevs (list): String abbreviations from wiktionary

    Returns:
        filtered (list): a subset of the list of abbreviations passed by
                         caller
    """

    # Remove any leading or trailing white spaces from abbreviations that user
    # may have typed accidentally in any input file
    abbrevs = list(map(lambda x: x.strip(), abbrevs))

    # Remove any weird but disruptive strings user could've added
    # to add.txt or remove.txt (e.g. '.' . ' .... ')
    # Regex pattern:
    # at least one alphanumeric character or underscore [a-zA-Z0-9_] followed
    # by zero or more periods; this pattern must be repeated at least once;
    # all strings must end with a period
    pattern = re.compile(r"[\w+\.*]+\.")
    filtered = list(filter(pattern.fullmatch, abbrevs))

    return filtered


def create_abbrevlist(wiki_abbrevs, add_abbrevs, remove_abbrevs):
    """Creates a final abbreviations list for abbreviations.txt

    Function adds and removes abbreviations from those retrieved
    on Wiktionary as per the contents of the arguments.

     Args:
        wiki_abbrevs (list): abbreviations from wiktionary.org
        add_abbrevs (list): abbreviations to add to wiki_abbrevs
        remove_abbrevs(list): abbreviations to remove from above lists

     Returns:
        A sorted list of string abbreviations

    """

    # Sets make it easier to remove duplicates and unwanted elements
    wikiset = set(wiki_abbrevs)
    addset = set(add_abbrevs)
    removeset = set(remove_abbrevs)

    # Merge two abbreviation sets together; duplicates removed automatically
    abbrevset = wikiset.union(addset)

    # Remove any abbreviations that may cause trouble for textanalysis module
    abbrevset = abbrevset.difference(removeset)

    # Sort the set before writing so it's easier for humans to visually
    # search and debug the list
    # Note that an ordered list is returned, not a set
    return sorted(abbrevset)


def run():
    """Executes web-scraping script

    Args:
        nil

    Raise:
        ValueError: if nothing scraped from wiktionary
    """

    # First page where abbreviations will start to be scraped
    abs_url = 'https://en.wiktionary.org/w/index.php?title=Category:' \
               'English_abbreviations&from=A'

    # Home page of site being scraped
    main_url = 'https://en.wiktionary.org'

    # Number of abbreviation pages needed for this script
    numpages = 21

    # The delay between fetching each page (in seconds)
    # If we scrape too fast, website might block us.
    delay = 1

    # Intro prompt
    print("Welcome to abbrevscrape!")
    print("This script will update abbreviations.txt with any new " +
          "abbreviations from Wiktionary.org.")

    # Give user choice to quit update: user may skip if done recently or
    # is unsure whether it is legal to scrape website
    print("***IMPORTANT!!***")
    print("Before scraping any website, verify that it's legal to do so by " +
          "reading its terms of service and/or checking its robots.txt file.")

    ans = input("Would you like to continue (Y/N)? ").strip()

    # Exit program if user said no or something unintelligible; carry-on if yes
    _carry_on(ans)

    # Get all the pages on wiktionary related to abbreviations
    wiki_abbrevs = scrape_wiki(abs_url, main_url, numpages, delay)

    # Want to make sure we have something to write to files below...
    if wiki_abbrevs:
        # Comment out this line if you want to keep acronyms from wiktionary
        wiki_abbrevs = filter_abbrevs(wiki_abbrevs)
    else:
        raise ValueError("List wiki_abbrevs empty.")

    try:
        print("Filtering and merging abbreviations...", end="")

        # Write filtered wiki_abbrevs to file
        with open("wiktionary.txt", 'w') as fout:
            for abbrev in wiki_abbrevs:
                fout.write(abbrev + '\n')

        # Load user-entered abbreviations to be added to abbreviations.txt
        with open("add.txt", 'r') as fin:
            add_abbrevs = fin.read().split('\n')

        # Load abbreviations that are too commonly used as nouns or verbs
        # These should not be in the abbreviation list we want for textanalysis
        with open("remove.txt", 'r') as fin:
            remove_abbrevs = fin.read().split('\n')

        # Last item in each list is a blank space; don't need that
        add_abbrevs.pop()
        remove_abbrevs.pop()

        # Filter the add_abbrevs and remove_abbrevs in case user added
        # abbreviations that don't end in a period
        add_abbrevs = filter_abbrevs(add_abbrevs)
        remove_abbrevs = filter_abbrevs(remove_abbrevs)

        # Add and remove any abbreviations from wiki_abbrevs
        abbrevlist = create_abbrevlist(wiki_abbrevs, add_abbrevs,
                                       remove_abbrevs)

        print("DONE!\nWriting abbreviations to abbreviations.txt...", end="")

        # Write final set to abbreviations.txt to be used by textanalysis
        with open("abbreviations.txt", 'w') as fout:
            for elem in abbrevlist:
                fout.write(elem + '\n')

        print("DONE!")

    except OSError as err:
        # Bad file IO
        print("OS error: {0}".format(err), file=sys.stderr)
        sys.exit()


# Script runs here
if __name__ == "__main__":

    try:
        run()

    except ValueError as err:
        print("Value error: {0}".format(err), file=sys.stderr)
