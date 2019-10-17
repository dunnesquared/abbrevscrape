Wiktionary Abbreviation Scraper

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

Pleae read "howto.txt" before writing abbreviations to "add.txt" or
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

ADDING ABBREVIATIONS TO 'add.txt' AND 'remove.txt'
==================================================
Just follow the examples already shown in the files: write an abbreviation
on a new line.

All abbreviations should end in a period. They will be filtered
out from abbreviations.txt if not.


TO RUN TEST SCRIPT
