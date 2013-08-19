# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup, SoupStrainer
import collections
import pycurl
import urllib
import google_play_key_words as gpkw
import json

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


class CallBackClass:
    def __init__(self):
        self.contents = ''

    def body_callback(self, buf):
        self.contents = self.contents + buf


class App(object):

    def __init__(self, page, query):
        self.urlString = self._makeQuery(query, page)
        self.HTML = self._getHTML(self.urlString)
        self.soup = self._getSoup(self.HTML)
        self.urls = self.soup('a', {'class': 'title'})  # get only the tags containing class with value title

    def _getHTML(self, url):
        return urllib.urlopen(url).read()

    def _makeQuery(self, q, p):
        return "https://play.google.com/store/search?q=" + q + "&c=apps" + "&start=" + str((p-1)*24) + "&num=24"

    def _getSoup(self, dt):
        return BeautifulSoup(dt, parseOnlyThese=SoupStrainer('a'))

    def get_all_app_urls(self):
        return [str(x['href']) for x in self.urls]

    def get_app_id(self, url):
        return url [url.find('=')+1:]

    def get_all_app_ids(self, url):
        x =[]
        for u in url:
            x.append(u[u.find('=')+1:])
        return x

    def get_all_app_titles(self):
        return [title['title'] for title in self.urls]

    def get_permissions(self, url):
        c = pycurl.Curl()
        cb = CallBackClass()
        c.setopt(c.URL, 'https://play.google.com/store/getdevicepermissions')

        c.setopt(c.WRITEFUNCTION, cb.body_callback)


        # id = id [id.find('=')+1:]
        self.id = self.get_app_id(url)

        c.setopt(c.HTTPHEADER, ['Cookie: PREF=ID=c696a2742cb72a8c:U=0dff6458d01a8cfc:FF=0:LD=en:TM=1375918333:LM=1375918708:S=wrEGpb7D1OTgSSGw; PLAY_PREFS=CgJVUxD7jYTZhSg:S:ANO1ljKp4n8fbXvp; NID=67=SVzphh8BjmJ4SrHU8mDsGqiWrAZYvQCP8y1OHJU5AvxS_aL1vtlSxeCY7PjvN05nuYKpC1E19RR7x_1pBdwKiC6wA2_nZrVheOAuUvC7OYojhKIZFejxCsZrxu7Yg8vvZntriX-7oFfdJPkEXzdDeQ5sCyajnilFkP0; SID=DQAAALwAAAAm5TOANcnCzV_K6z5ZtWWORBGWfi7CvJP9wOXPrnqpWBZUV0TdQZWNXr2WNnU7M4fhT5BEcP-Cgs1GAWdSJQ8eWqwgQ-8mLrs1VcKHZelFb7q_I0ZhsXeQ1tRL2wz5S7mR9dGG0TqnYB5LxXlm_eBdiZN_mUKjv8gq-Ykwyc9rxYiX_n06i0FeHDoxuA981j3_EdqxRTz_bK6QIaIjEFe_HMxo2dmgreIhQkMcT8X2rKaTfbkkw-s4au6GOPGcbfo; HSID=AcoTQHHYYN42Op8NL; SSID=APggUeOIfgSUN32Oz; APISID=ef4kvsQBkVFl8VM6/Am3Lk-MxdBSHQUgRc; SAPISID=x-zWa70_HEVoHIF3/A5HVApVB55u0DSr7f;PLAY_ACTIVE_ACCOUNT=ICrt_XL61NBE_S0rhk8RpG0k65e0XwQVdDlvB6kxiQ8=applidmail@gmail.com'])

        c.setopt(c.POSTFIELDS, 'id='+self.id+'&xhr=1&token=kGxukBkmCXTZFIG5Tk4fzMHBtsw%3A1375918986927')
        c.setopt(c.POST, 1)
        c.perform()
        c.close()

        mystring = cb.contents.decode('unicode-escape')
        # trim string
        _beg = str(mystring).find('<div')
        _end = str(mystring).rfind('</div>')
        mystring = mystring[_beg:]
        mystring = mystring[:(len(mystring)-_end)+15]
        # end - trim

        # get permissions THIS IS RENDERED IN HTML no longer need to remove div tags
        # soup = BeautifulSoup(mystring)
        # items = soup('div', {'class': 'perm-description'})

        # return permissions
        return mystring

f = open('apps.json', 'a')

apps_array = []

for index in range(0, 100):

    for page in range(0, 3):
        apps = App(page, gpkw.terms[index])
        # print gpkw.terms[index]
        for app in range(0, len(apps.get_all_app_titles())):
            apps_array.append({"search-term": gpkw.terms[index],
                               "name": apps.get_all_app_titles()[app],
                               "package-id": apps.get_all_app_ids(apps.get_all_app_urls())[app],
                               "permissions": apps.get_permissions(apps.get_all_app_urls()[app])})

f.write(json.dumps(apps_array, indent=4))
# test output
# print json.dumps(apps_array, indent=4)

# TODO-format "keyword" -> [list of package names in rank order] -> [list of permissions for each package, as a messy string]
