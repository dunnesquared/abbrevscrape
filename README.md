# Wiktionary Abbreviation Scraper
> Scrape abbreviations from wikitionary.org

The purpose of this script is to create a text file containing a list of
abbreviations commonly used in English. The intended user of this list is
module "textanalysis", which uses the abbreviation file to help extract
sentences from a a text.

Abbreviations are scraped from Wiktionary.org. Continuous thanks to the
many Wikimedia contributors who make it possible to write scripts like
these!

## Installation

OS X & Linux:

```sh
npm install my-crazy-module --save
```

Windows:

```sh
edit autoexec.bat
```

## Usage example

Assuming a working internet connection, run the script from the root of the
project directory; type the following (or the equivalent) on the command line:

```sh
python3 abbrevscrape.py
```

Wiktionary leaves out some common abbreviations such as Mr. or Dr. As such,
users may want to add abbreviations that don't appear on the site. This can
be easily by entering each abbreviation on a newline. The script will then
add these to the final output file, 'abbreviations.txt.' Note that all
abbreviations must be single words that end in a period–the script will filter
everything else out

```sh
Lm.
Vzr.
Hs.
...
```

Conversely, you may want to remove abbreviations that are scraped from
wiktionary. Rather than delete them from 'abbreviations.txt', just add them
to 'remove.txt' in the method described above. The script will then automati-
cally filter them out and will not appear in the final output file.

## Development setup

Describe how to install all development dependencies and how to run an automated test-suite of some kind. Potentially do this for multiple platforms.

```sh
make install
npm test
```

## Release History
* 0.1.0
    * The first proper release


## Meta

Your Name – YourEmail@example.com

Distributed under the GNU GPLv3 license. See ``LICENSE`` for more information.

[https://github.com/yourname/github-link](https://github.com/dbader/)

## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/yourname/yourproject/wiki
