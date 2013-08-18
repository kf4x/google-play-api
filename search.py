from BeautifulSoup import BeautifulSoup
import collections
import urllib2

__author__ = 'Javier'


"""
Base URL = https://play.google.com/store/search

Search
?q=nameofapp

Media Type (apps, books, movies)
&c=apps

Final URL
https://play.google.com/store/search?q=twitter&c=apps

Page >1  increment start by 24
https://play.google.com/store/search?q=twitter&c=apps&start=24&num=24
"""

# util these are little fns that klajhdfakjdfnkljandfj


def getHTML(url):
    return urllib2.urlopen(url).read()


def makeQuery(q, p):
    return "https://play.google.com/store/search?q=" + q + "&c=apps" + "&start=" + str((p-1)*24) + "&num=24"
# end-util


class Page(object):
    def __init__(self, page, query):
        self.urlString = makeQuery(query, page)
        self.HTML = getHTML(self.urlString)

    def _get_script_tag(self):
        soup = BeautifulSoup(self.HTML)
        items = soup('li', {'class': 'search-results-item'})  # each app is under considered an 'item'
        return items


class Search(object):   # search class is used to hold the search (interacts with user)

    def __init__(self, search='twitter'):  # default search term is 'twitter'
        self.search = search

    def _get_page(self, page=1):
        self.page = Page(page, self.search)
        return self.page

    def get_first(self):    # a convenience method
        self._get_page()

        return self.page.get_all_apps()[0]  # returns first app in list

    def get_all(self):
        self._get_page()

        return self.page.get_all_apps()  # returns list of all(24) apps on the page

    def get_page(self, page):   # allows to specify page number
        self._get_page(page)

        return self.page.get_all_apps()  # returns list of apps on specified page

    def get_HTML(self):
        return self.page.HTML

    def compare_page(self, page):
        # using http://docs.python.org/2/library/collections.html
        full = self.get_page(page)

        list = []

        for app in range(0,24):
            list.extend(full[app].get_permission())

        return collections.Counter(list)