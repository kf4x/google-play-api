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

fetched = False


class App(object):  # App class is used to hold information about an individual app scraped from the app store

    def __init__(self, itemHTML):
        self.bs = itemHTML
        self._set_name()
        self._set_perm()

    def _set_name(self):
        link = self.bs('a', {'class': 'title'})[0]  # equivalent of find all 'a tags' with class title
        self._name = link.contents[0]

    def _set_perm(self):
        link = self.bs('div', {'class': 'details goog-inline-block'})[0]
        prem_link = "https://play.google.com/"+link.contents[0]['href']
        self._setting_permission(prem_link)

    def get_name(self):
        return self._name

    def get_permission(self):
        return self._permission_list

    def _setting_permission(self, url):  # intermediary step that collects all the permissions from the page
        self._permission_list = []
        HTML = getHTML(url)
        soup = BeautifulSoup(HTML)

        soup_list = soup('li', {'class': 'doc-permission-group'})

        for x in soup_list:
            a = x('div', {'class': 'doc-permission-description'})[0]  # TODO also iterate through this
            self._permission_list.append(a.contents[0])

        # print self._perm


class Page(object):  # page class to hold page of apps
    def __init__(self, page, query):
        self.urlString = makeQuery(query, page)
        self.HTML = getHTML(self.urlString)

    def _get_apps(self):

        soup = BeautifulSoup(self.HTML)
        items = soup('li', {'class': 'search-results-item'})  # each app is under considered an 'item'
        return items

    def get_all_apps(self):
        appArray = []

        items = self._get_apps()
        # as of now they are html

        for app in items:
        #   need to turn into app object and use app class

            appArray.append(App(app))

        return appArray


class Search(object):   # search class is used to hold the search (interacts with user)

    def __init__(self, search='twitter'):  # default search term is 'twitter'
        self.search = search
        self.fetched = False

    def _get_page(self, page=1):
        self.page = Page(page, self.search)
        return self.page

    def get_first(self):    # a convenience method

        if self.fetched is False:
            self._get_page()
            self.fetched = True

        return self.page.get_all_apps()[0]  # returns first app in list

    def get_all(self):

        if self.fetched is False:
            self._get_page()
            self.fetched = True

        return self.page.get_all_apps()  # returns list of all(24) apps on the page

    def get_page(self, page):   # allows to specify page number

        # if page > 1:
        self._get_page(page)
        self.fetched = True
        # elif page == 1 and self.fetched is False:
        #     self._get_page()
        #     self.fetched = True

        return self.page.get_all_apps()  # returns list of apps on specified page

    def get_HTML(self):
        return self.page.HTML

    def compare_all(self):
        h = list(self.page.get_all_apps())
        aa = set(h)
        print "The first app has permissions\n"
        print aa
        print "\nThe similarities\n"
        for x in range(1, 24):
            print aa.intersection(list(self._all))

        print "\nThe differences\n"
        for x in range(1, 24):
            print aa.union(self.page.get_all_apps()[x]) - aa.intersection(self.page.get_all_apps()[x])



# i = Search("twitter")
# a = i.get_first()
# print a.get_name()
# print a.get_permission()

# p = i.get_page(2)
# for s in range(0,24):
#     print p[s].get_name(), p[s].get_permission()
# print a.get_permission()
