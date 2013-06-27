#!/usr/bin/env python


from flask import Flask, jsonify, request
from BeautifulSoup import BeautifulSoup
import collections
import urllib

application = app = Flask('wsgi')

@app.route('/')
def hello():
    return "Hello World!"


@app.route('/app/search', methods=['GET'])
def s_apps():
    q = request.args.get('q', None)  # ?q=some-value
    p = request.args.get('p', 1)

    search = Search(q)

    page = search.get_page(p)

    app_array = []

    apps = {
        'apps': app_array
    }

    #iterate through the apps on page 2. there are 24 apps/page
    for a in range(0,24):

        app_array.append({'name': page[a].get_name(), 'permissions' : page[a].get_permission()})
        # app_data.clear()
        # print page[a].get_name(), page[a].get_permission()

    resp = jsonify(apps)
    resp.status_code = 200
    return resp

@app.route('/app/compare', methods=['GET'])
def c_apps():
    q = request.args.get('q', 'twitter') # ?q=some-value
    p = request.args.get('p', 1)

    search = Search(q)

    # compare returns a Counter
    counter = search.compare_page(p)


    resp = jsonify(counter.most_common(30))
    resp.status_code = 200
    return resp


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
        # using http://docs.python.org/2/library/collections.html
        full = self.get_page(page)

        list = []

        for app in range(0,24):
            list.extend(full[app].get_permission())

        return collections.Counter(list)


def getHTML(url):
    return urllib.urlopen(url).read()


def makeQuery(q, p):
    return "https://play.google.com/store/search?q=" + q + "&c=apps" + "&start=" + str((p-1)*24) +"&num=24"


if __name__ == '__main__':
    app.run(debug=True)