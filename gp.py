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
            a = x('div', {'class': 'doc-permission-description'})

            if len(a) > 0:
                for i in range(0, len(a)):
                    self._permission_list.append(str(a[i].contents[0]))

        self._permission_list.sort()


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
        self._get_page(page)
        self.fetched = True

        return self.page.get_all_apps()  # returns list of apps on specified page

    def get_HTML(self):
        return self.page.HTML

    def compare_page(self, page):
        # TODO redo this crap
        full = self.get_page(page)
        '''
            1 get all the unique values
            2 using unique array count array with everything

            #1 containing similarities
            #1 containing differences

        '''

        list = []

        for app in range(0,24):
            list.extend(full[app].get_permission())

        print list
