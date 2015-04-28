import requests
from requests import Session
from bs4 import BeautifulSoup, SoupStrainer
import ast
import json
import logging


__author__ = "Javier Chavez"
__email__ = 'javierc@cs.unm.edu'

_URL = "https://play.google.com/store/getreviews"
_USER_AGENT = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
_ACCEPT = "*/*"
_ACCEPT_ENCODING = "gzip, deflate"
_ACCEPT_LANGUAGE = "en-US,en;q=0.8"
_CACHE_CONTROL = "no-cache"
_CONTENT_LENGTH = "129"
_CONTENT_TYPE = "application/x-www-form-urlencoded;charset=UTF-8"
_ORIGIN = "https://play.google.com"



_COOKIE = {"SID": "",
           "SAPISID": "",
           "PREF": "",
           "PLAY_PREFS": "",
           "PLAY_ACTIVE_ACCOUNT": "",
           "NID":"",
           "HSID": "",
           "APISID": "",
           "_gat": "",
           "_ga": ""}


class Search(object):
    """Search Class that allows searching for apps in play store"""

    def __init__(self, session, key_word='', page=1):
        """Inits Search

        Args:
            session: session object from requests.session
            key_word: word or app or some text you want to search with
            page: what page of the search will be returned.
        """
        self.session = session
        self.key_word = key_word
        self.bs_links = []
        if key_word:
            self._search(key_word, page)

    def get_results(self):
        """Get all the apps from the page

        Returns:
            An array filled with App objects, for example:
            [Twitter, Facebook]
        """
        apps = []
        for app in self.bs_links:
            index = app['href'].find('=')
            aid = app['href'][index+1:]
            apps.append(App(self.session,
                            aid,
                            key_word=self.key_word,
                            url=app['href'],
                            name=app['title']))

        logging.debug(str(len(apps)) + " returned for " + self.key_word)
        return apps

    def search(self, key_word, page=1):
        """Search and return apps from search

        """
        self._search(key_word, page)
        return self.get_results()

    def _search(self, key_word, page=1):
        #url= "https://play.google.com/store/search?q=" + key_word + "&c=apps" + "&start=" + str((page-1)*24) + "&num=24"
        # no longer support pagination
        url = "https://play.google.com/store/search?q=" + key_word + "&c=apps"
        req = self.session.get(url=url)
        soup = BeautifulSoup(req.content,
                             parse_only=SoupStrainer('a', href=True))

        self.bs_links = soup.findAll('a', {'class': 'title'})
        #print(len(self.bs_links))

    def __str__(self):
        return "Search"

    def __repr__(self):
        return self.__str__()


class App(object):
    """Class that represents a android app
    """

    def __init__(self, session, app_id, **kwargs):
        """Inits a App object
        Args:
            session: session object from requests.session
            app_id: string id of the app (package)
        """
        self.session = session
        # attributes of an app
        self.url = ''
        self.name = ''
        self.developer = ''
        self.package = app_id
        self.description = ''
        self.installs = ''
        self.total_ratings = ''
        self.permissions = []
        self.rating = ''
        self.key_word = ''
        self.screenshots = []
        self.icon = ''
        self.genre = ''
        self.size = ''
        self.price = ''
        self.pub_date = ''
        self.category = ''
        self.reviews = []
        self.__is_populated = False
 
        for key, value in kwargs.items():
            setattr(self, key, value)
        # preappending host
        self.url = 'https://play.google.com' + self.url
        # TODO - implement dispatcher
        # dispatcher = {
        #     'url': _set_url,
        #     'name': _set_name,
        #     'developer': _set_dev,
        #     'package': _set_package,
        #     'description': _set_description,
        #     'installs': _set_installs,
        #     'total_ratings': _set_ratings,
        #     'permissions': _set_perms,
        #     'rating': _set_rating,
        #     'key_word': _set_kw,
        #     'screenshots': _set_ss,
        #     'icon': _set_icon,
        #     'price': _set_price,
        #     'pub_date': _set_pd,
        #     'category': _set_cat,
        #     'reviews': _set_reviews
        # }

    def populate_fields(self, exclude=[]):
        """Populate the apps fields. Sometimes this can
        take some time which is why you must call it when
        you are ready.
        """
        self.get_permissions(exclude)
        #self.populate_data()


    def get_permissions(self, exclude=[]):
        """Get all the permissions for this app """
        # if the permissions are already set do not go fetch
        if self.__is_populated:
            return True

        # exlude the fields that do not pretain to app
        attrs = set(self.__dict__.keys()) - {'session',
                                             '__is_populated'}

        # if exclude has something in it remove from attrs
        if exclude:
            # list used to populate this class
            # getting the symmetric difference
            attrs = attrs - (set(exclude))


        # everything needs to be set inorder to get permissions
        if not self.package or not self.session.header_que or not self.session.cookie_que:
            raise Exception('You need proper app_id, headers, and cookie!')

        # log
        logging.info('Requesting premissions from google')

        #url = 'https://play.google.com/store/getdevicepermissions?authuser=0'
        url = 'https://play.google.com/store/xhr/getdoc?authuser=0'
        # setting referer for header 
        ref = {'Referer':'https://play.google.com/store/apps/details?id='+self.package}

        # I am copying the cookie que into a variable
        cookies = self.session.cookie_que.copy()

        # Add the cookie-q to the session object
        requests.utils.add_dict_to_cookiejar(self.session.cookies, cookies)

        # add the referer to the header-que
        self.session.header_que.update(ref)

        # add the id to the session-que
        self.session.param_que.update({'ids':str(self.package)})

        # get the headers and params ready to be sent with request
        headers = self.session.header_que
        payload = self.session.param_que

        # setting everything for post
        data = self.session.post(url=url,
                                 headers=headers,
                                 data=payload)
        # close this since we will be making more calls
        self.session.close()

        # report status code
        logging.info("Request complete, status code: " + str(data.status_code))

        # decode the return binary data
        _arr = data.content.decode("utf-8")
 
        # convert javascript array into python list
        _arr = _arr.replace(")]}\'\n\n", "")
        _arr = _arr.replace('\\"', "\u0027")
        _arr = _arr.replace(",,", ",None,")
        _arr = _arr.replace(",, ", ",None,")
        _arr = _arr.replace(", ,", ",None,")
        _arr = _arr.replace(",,", ",None,")
        _arr = _arr.replace("[,", "[None,")
        _arr = _arr.replace('\r', ' ').replace('\n', ' ')
        _arr = _arr.replace('\\"', "\u0027")
        
        _app_array = ast.literal_eval(_arr)
        #print(json.dumps(_app_array, indent=4))
        _app_obj = _app_array[0][2][0][55]
        _app_obj_keys = _app_obj.keys()
        _app_obj_f_k = list(_app_obj_keys)[0]
        # print(list(_app_obj_keys)[0])
        _app_obj_arr = _app_obj[_app_obj_f_k]
        # print(json.dumps(_app_array, indent=4))
        #_app_obj_arr = _app_obj
        logging.debug("Conversion JS array ")

        # TODO - check to see if attr is in attrs list
        # if it is then set it
        # else ignore
        if 'description' in attrs:
            self.description = _app_array[0][2][0][9]
        if 'category' in attrs:
            self.category = _app_array[0][2][0][14][0][0]
        if 'rating' in attrs:
            self.rating = _app_array[0][2][0][16]
        if 'total' in attrs:
            self.total_ratings = _app_array[0][2][0][17]
        if 'name' in attrs:
            self.name = _app_array[0][2][0][8]
        if 'icon' in attrs:
            self.icon = _app_array[0][2][0][18]
        if 'pub_date' in attrs:
            self.pub_date = _app_obj_arr[2]
        if 'price' in attrs:
            self.price = _app_array[0][2][0][13][0][1]
        if 'size' in attrs:
            self.size = _app_obj_arr[4] or "varies"
        if 'developer' in attrs:
            self.developer = _app_obj_arr[0][0]
        if 'url' in attrs:
            self.url = _app_array[0][2][0][7]
        if 'installs' in attrs:
            self.installs = (_app_obj_arr[5] or "0") + " - " + (_app_obj_arr[6] or "5")
        
        if 'permissions' in attrs:
            # types of permissions ....
            stand_p = _app_obj_arr[1][0]
            other_p = _app_obj_arr[1][1]
            custom_p = _app_obj_arr[1][2]
            _permarr = []


            for a in stand_p:
                # print a
                for b in a[1]:
                    _permarr.append(b[0])
            for a in other_p:
                # print a
                for b in a[1]:
                    _permarr.append(b[0])
            for a in custom_p:
                _permarr.append(a[0])

            self.permissions = _permarr            

        if 'screenshots' in attrs:
            for a in _app_array[0][2][0][20]:
                self.screenshots.append(a[4])

        if 'reviews' in attrs:
            self.reviews = self._get_reviews()

        self.__is_populated = True
        return True

    def _set_perms(self):
        # move permission stuff here.
        pass

    def _get_reviews(self):
        url = 'https://play.google.com/store/getreviews?authuser=0'
        ref = {'Referer':'https://play.google.com/store/apps/details?id='+self.package}

        # this can be removed
        cookies = self.session.cookie_que.copy()
        # preparing cooies
        requests.utils.add_dict_to_cookiejar(self.session.cookies, cookies)

        # add the referer to header
        self.session.header_que.update(ref)
        # add to param
        self.session.param_que.update({'id': str(self.package),
                                       'reviewType': 0,
                                       'pageNum': 0,
                                       'reviewSortOrder': 4})

        headers = self.session.header_que
        payload = self.session.param_que

        # setting everything for post
        review_data = self.session.post(url=url,
                                        headers=headers,
                                        data=payload)
        
        # report status code
        logging.info("Request complete, status code: " + str(review_data.status_code))
        self.session.close()
        # import emoji .decode('unicode-escape')
        raw = review_data.content.replace(b'\\"', b"\u0027")
        rev_arr = raw.decode('unicode-escape')

        # convert javascript array into python list
        rev_arr = rev_arr.replace(")]}\'\n\n", "")
        #rev_arr = rev_arr.replace('\\"', "\u0027")
        rev_arr = rev_arr.replace(",,", ",None,")
        rev_arr = rev_arr.replace(",, ", ",None,")
        rev_arr = rev_arr.replace(", ,", ",None,")
        rev_arr = rev_arr.replace(",,", ",None,")
        rev_arr = rev_arr.replace("[,", "[None,")
        rev_arr = rev_arr.replace('\r', ' ').replace('\n', ' ')

        _app_array = ast.literal_eval(rev_arr)

        #print(len(_app_array))

        return _app_array[0][2]

    def populate_data(self):
        """Helper to set the rest of the attributes of the this app"""
        logging.error("Calling non impl. method")
        raise Exception("Not working")

        # url to reviews
        # https://play.google.com/store/getreviews
        item_props = [
            'datePublished',
            'fileSize',
            'numDownloads',
            'softwareVersion',
            'contentRating',
            'image',
            'url',
            'genre',
            'price',
            'topDeveloperBadgeUrl',
            'screenshot',
            'ratingValue',
            'ratingCount',
            'description'
        ]
        
        html = self.session.get(self.url)
        
        soup = BeautifulSoup(html.content.decode('unicode-escape'))
        # using find since it only returns a single obj
        # self.description = soup.find('div', {'itemprop': 'description'}).contents
        
        # get all the tags that has attribute itemprop and
        # the value of itemprop is in item_props list
        all_meta = soup(lambda tag: 'itemprop' in tag.attrs and
                        dict(tag.attrs)['itemprop'] in item_props)

        screenshots = []
        # TODO: need to make this more generic
        for x in all_meta:

            item = x.get('itemprop')
            if 'datePublished' in item:
                self.pub_date = x.contents[0]
            # elif 'fileSize' in item:
            #    print('filesize '+x.contents[0])
            elif 'numDownloads' in item:
                self.installs = x.contents[0]
            elif 'image' in item:
                self.icon = x.get('src')
            elif 'screenshot' in item:
                screenshots.append(x.get('src'))
            elif 'price' in item:
                self.price = x.get('content')
            elif 'genre' in item:
                self.genre = x.contents[0]
            elif 'ratingValue' in item:
                self.rating = x.get('content')
            elif 'ratingCount' in item:
                self.total_ratings = x.get('content')
            # elif 'description' in item:
            #     desc = x.find('div', {'class':'id-app-orig-desc'})
            #     print type(desc)
            #     self.description = ''
                
                
            

        self.screenshots = screenshots
        del screenshots
        del all_meta
        return True
        
    def to_dict(self):
        app_dict = self.__dict__
        _keys = app_dict.keys()
        if 'session' in _keys:
            del app_dict['session']
        if '_App__is_populated' in _keys:
            del app_dict['_App__is_populated']
        return app_dict


    def __str__(self):
        return "App"

    def __repr__(self):
        return self.__str__()

    def ga(*args):
        return getattr(*args)

    __getitem__ = ga
    
class PlayStore(Session):
    """Main wrapper for the google play store api.
    The class is subclassing Session from requests.
    """

    def __init__(self, cookie, token=''):
        """Inits PlayStore with cookie and token. Would
        strongly suggest only using cookie, otherwise you
        will need to supply a much larger cookie for
        that see googleplaystore._cookie.
        
        Args:
            cookie: a dictionary for example:
                { "PLAY_PREFS": "value",
                  "NID"       : "value",
                  "_gat"      : "value",
                  "_ga"       : "value"
                }
            token: string of a token
        """
        if token or cookie:
            self.set_creds(token=token, cookie=cookie)
        else:
            self.cookie_que = {}
            self.param_que = {}

        # default headers que'd 
        self.header_que = {
            "accept": _ACCEPT,
            "accept-encoding": _ACCEPT_ENCODING,
            "accept-language": _ACCEPT_LANGUAGE,
            "content-length": _CONTENT_LENGTH,
            "content-type": _CONTENT_TYPE,
            "origin": _ORIGIN,
            "pragma": _CACHE_CONTROL,
            "dnt": 1,
            "user-agent": _USER_AGENT
        }

        super(PlayStore, self).__init__()

    def set_creds(self, token='', cookie={}):

        # setting which will be used for permissions/reviews
        self.cookie_que = cookie
        self.param_que = {
            'xhr': 1,
        }
    def get_app(self, app_id):
        """Get app by its package id
        
        Args:
            app_id: String of the package com.google.example

        Returns:
            App object
        """
        return App(self, app_id)

        
    def search(self, search_term='', page=1):
        """Search the play store with some keyword. NOTE: if 
        search_term is empty a search object will be returned.

        Args:
            search_term: string of the keyword, "twitter"
            page: integer the page you would like

        Returns:
            Search object
        """
        return Search(self, search_term, page)
        

