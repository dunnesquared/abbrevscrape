# Abbrevscrape

Abbrevscrape is a Python script that scrapes abbreviations from Wiktionary.org
and writes them to a local text file. I wrote the script because I wanted a
list of abbreviations for another project of mine,
[Le Guin Sentence Word Counter][LGSWC]. LGSWC uses a text file generated by
abbrevscrape to help it extract sentences from a text.

## Setting up the development environment

> It is highly recommended that you are in a virtual environment before doing any of the below.

To use abbrevscrape, first clone the [repository][repo] and then run the
following command on your console:

```sh
python setup.py install
```

Run `pip list` to see whether the testing framework `nose` was installed with
the other packages abbrevscrape depends on. If not, you can download it at
PyPI with

```sh
pip install nose
```

To run the test script, simply run

```sh
nosetests
```


## Running abbrevscrape

The script was designed to work in situ, i.e. from the root of the project
directory. If you don't run the script from here, it won't find the
necessary input and output files it needs to complete
its work. All such files are stored in the root-level directory
folder `data`.

So, assuming you're at the project's root and have a working internet
connection, you can run the script as follows:

```sh
python3 abbrevscrape.py
```

The results are stored in two files: `wiktionary.txt` and `abbreviations.txt`.
The former file contains any Wiktionary abbreviation that is a single
word which ends with a period, whereas the latter is the intersection of these
abbreviations with those specified in user input files `add.txt` and
`remove.txt`.

LGSWC uses `abbreviations.txt` for its processing.

## Adding entries to `add.txt` and `remove.txt`

It may be the case that Wiktionary.org doesn't have all the abbreviations
you might need. For example, the site seems to be missing common honorifics
such as 'Mr.' and 'Dr.', both of which I required for LGSWC.

To have additional abbreviations appear in `abbreviations.txt`, you'll need to
enter each one on a newline in `add.txt`. There are entries already in the file
you can use as a guide, but, for the sake of completeness, here is an example.

```sh
Lmin.
Gyzr.
Hsoot.
...
```

Conversely, you may want to remove abbreviations that are scraped from
Wiktionary.org. Rather than delete them from `abbreviations.txt`, just enter
them in `remove.txt` using the method described above; the script will
automatically filter them out.

## Meta

Distributed under the MIT license. See ``LICENSE`` for more information.
Copyright (c) 2019 Alexander Dunne


<!-- Markdown link & img dfn's -->
[LGSWC]: https://github.com/dunnesquared/leguinsentencewordcounter
[repo]: https://github.com/dunnesquared/abbrevscrape
