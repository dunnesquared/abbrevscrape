from nose.tools import *
from abbrevscrape import *
import requests


def test_carry_on():
    import abbrevscrape as abscrape

    # All possible negative responses with spaces
    ans = '   N    '
    assert_raises(SystemExit, abscrape._carry_on, ans.strip())

    ans = '   n   '
    assert_raises(SystemExit, abscrape._carry_on, ans.strip())

    ans = '   no   '
    assert_raises(SystemExit, abscrape._carry_on, ans.strip())

    ans = '   No   '
    assert_raises(SystemExit, abscrape._carry_on, ans.strip())

    # Invalid response
    ans = '   N o   '
    assert_raises(SystemExit, abscrape._carry_on, ans.strip())


def test_scrape_wiki():
    # Default values
    abs_url = 'https://en.wiktionary.org/w/index.php?title=Category:' \
               'English_abbreviations&from=A'
    main_url = 'https://en.wiktionary.org'
    numpages = 21
    delay = 1


    # numpages = 0
    numpages = 0
    assert_raises(ValueError, scrape_wiki, abs_url, main_url, numpages, delay)

    # numpages < 0
    numpages = -1
    assert_raises(ValueError, scrape_wiki, abs_url, main_url, numpages, delay)

    # 0 < delay < 1  => should not happen
    numpages = 21 # reset
    delay = 0.5
    assert_raises(ValueError, scrape_wiki, abs_url, main_url, numpages, delay)

    # 0 < delay
    delay = -1
    assert_raises(ValueError, scrape_wiki, abs_url, main_url, numpages, delay)

    # bad abs_url: non-sensical
    delay = 1 # reset
    abs_url = 'yo'
    assert_raises(SystemExit, scrape_wiki, abs_url, main_url, numpages, delay)

    # bad abs_ur: wrong site, but scrapable
    abs_url = 'https://www.nytimes.com'
    assert_raises(SystemExit, scrape_wiki, abs_url, main_url, numpages, delay)

    # bad abs_ur: wrong site, forbidden to access
    abs_url = 'https://public.oed.com/how-to-use-the-oed/abbreviations/'
    assert_raises(SystemExit, scrape_wiki, abs_url, main_url, numpages, delay)

    # bad main_url: non-sensical
    abs_url = 'https://en.wiktionary.org/w/index.php?title=Category:' \
               'English_abbreviations&from=A' # reset
    main_url = 'yo'
    assert_raises(SystemExit, scrape_wiki, abs_url, main_url, numpages, delay)

    # bad main_url: wrong site
    main_url = 'https://www.nytimes.com'
    assert_raises(SystemExit, scrape_wiki, abs_url, main_url, numpages, delay)


def test_is200():
    import abbrevscrape as abscrape

    # status code == 200
    # status code != 200
    assert_equal(abscrape._is200(200), True)
    assert_equal(abscrape._is200(-200), False)


def test_filter_abbrevs():
    # Valid input: something to filter
    abbrevs = ['ABC', 'DEF.', 'GHI']
    expected = ['DEF.']
    assert_equal(filter_abbrevs(abbrevs), expected)

    # Valid input: nothing to filter
    abbrevs = ['ABC.', 'DEF.', 'GHI.']
    expected = ['ABC.', 'DEF.', 'GHI.']
    assert_equal(filter_abbrevs(abbrevs), expected)

    # Empty list
    abbrevs = []
    expected = []
    assert_equal(filter_abbrevs(abbrevs), expected)

    # Nasty abbrevs that would mess up textanalysis big time
    abbrevs = ['.', '   .   ', '?. ']
    expected = []
    assert_equal(filter_abbrevs(abbrevs), expected)

    # Test that failed...
    abbrevs = ['a', 'bc.a', 'cd', 'b.c.']
    expected = ['b.c.']
    assert_equal(filter_abbrevs(abbrevs), expected)



def test_create_abbrevlist():
    # Default
    wiki_abbrevs = ['X.', 'Y.', 'Z.']
    add_abbrevs = ['A.', 'B.', 'C.', 'D.']
    remove_abbrevs = ['B.']

    # Typical, valid input
    expected = sorted({'A.', 'C.', 'D.', 'X.', 'Y.', 'Z.'}) # need to sort regardless; order won't be preserved otherwise
    assert_equal(create_abbrevlist(wiki_abbrevs, add_abbrevs, remove_abbrevs), expected)

    # Remove an abbrev that is not in union
    remove_abbrevs = ['F.']
    expected = sorted({'A.', 'B.', 'C.', 'D.','X.', 'Y.', 'Z.'})
    assert_equal(create_abbrevlist(wiki_abbrevs, add_abbrevs, remove_abbrevs), expected)

    # Empty wikiabbrevs
    remove_abbrevs = ['B.'] # reset
    wiki_abbrevs = []
    expected = sorted({'A.', 'C.', 'D.'})
    assert_equal(create_abbrevlist(wiki_abbrevs, add_abbrevs, remove_abbrevs), expected)

    # Empty addabbrevs
    wiki_abbrevs = ['X.', 'Y.', 'Z.'] # reset
    add_abbrevs = []
    expected = sorted({'X.', 'Y.', 'Z.'})
    assert_equal(create_abbrevlist(wiki_abbrevs, add_abbrevs, remove_abbrevs), expected)

    # Empty removeabbrevs
    add_abbrevs = ['A.', 'B.', 'C.', 'D.'] # reset
    remove_abbrevs = []
    expected = sorted({'A.', 'B.', 'C.', 'D.', 'X.', 'Y.', 'Z.'})
    assert_equal(create_abbrevlist(wiki_abbrevs, add_abbrevs, remove_abbrevs), expected)

    # All empty lists
    wiki_abbrevs, add_abbrevs, remove_abbrevs = [], [], []
    expected = sorted({}) # sorted alwats returns a list
    assert_equal(create_abbrevlist(wiki_abbrevs, add_abbrevs, remove_abbrevs), expected)
