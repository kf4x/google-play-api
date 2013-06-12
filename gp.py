from BeautifulSoup import BeautifulSoup
from util import *

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


class App(object):

    def __init__(self, itemHTML):
        self.bs = itemHTML
        self._set_name()
        self._set_prem()

    def _set_name(self):
        link = self.bs('a', {'class': 'title'})[0]
        self._name = link.contents[0]

    def _set_prem(self):
        link = self.bs('div', {'class': 'details goog-inline-block'})[0]
        prem_link = "https://play.google.com/"+link.contents[0]['href']
        self._setting_permission(prem_link)

    def get_name(self):
        return self._name

    def get_premis(self):
        return self._perm

    def _setting_permission(self, url):
        HTML = getHTML(url)
        soup = BeautifulSoup(HTML)

        self._perm = soup('li', {'class': 'doc-permission-group'})

        print self._perm
    def __iter__(self):
        return iter(self._iterable)

class Page(object):
    def __init__(self, page, query):
        self.page = page
        self.urlString = makeQuery(query)
        self.HTML = getHTML(self.urlString)
        # print self.HTML

    def _get_apps(self):

        soup = BeautifulSoup(self.HTML)
        items = soup('li', {'class': 'search-results-item'})
        return items

    def get_all_apps(self):
        appArray = []

        items = self._get_apps()
        # as of now they are html

        for app in items:
        #   need to turn into app object and use app class
            appArray.append(App(app))

        return appArray


class Search(object):
    def __init__(self, search='twitter'):
        self.search = search

    def _get_page(self, page=1):
        self.page = Page(page, self.search)
        return self.page

    def get_first(self):

        page = self._get_page()
        return page.get_all_apps()[0]

    def get_HTML(self):
        return self.page.HTML

    def compare_all(self):
        h = list(self.get_first())
        aa = set(h)
        print "The first app has permissions\n"
        print aa
        print "\nThe similarities\n"
        for x in range(1, 24):
            print aa.intersection(self.page.get_all_apps()[x])

        print "\nThe differences\n"
        for x in range(1, 24):
            print aa.union(self.page.get_all_apps()[x]) - aa.intersection(self.page.get_all_apps()[x])

# helpers if needed
def callback(cb):
    # call the fn
    cb()


def showResults(string):
    print string

i = Search("twitter")
a = i.get_first()
# i.compare_all()
print a.get_premis()
