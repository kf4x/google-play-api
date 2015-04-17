import requests
from requests import Session
from requests.cookies import cookiejar_from_dict
from bs4 import BeautifulSoup, SoupStrainer
import ast
import json

__author__ = "Javier Chavez"


_URL = "https://play.google.com/store/getreviews"
_USER_AGENT = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
_ACCEPT = "*/*"
_ACCEPT_ENCODING = "gzip, deflate"
_ACCEPT_LANGUAGE = "en-US,en;q=0.8"
_CACHE_CONTROL = "no-cache"
_CONTENT_LENGTH = "129"
_CONTENT_TYPE = "application/x-www-form-urlencoded;charset=UTF-8"
_ORIGIN = "https://play.google.com"



_COOKIE = { "SSID": "",
            "SID": "",
            "SAPISID": "",
            "PREF": "",
            "PLAY_PREFS": "",
            "PLAY_ACTIVE_ACCOUNT": "",
            "NID":"",
            "HSID": "",
            "APISID": "",
            "_gat": "",
            "_ga": "" }



def memoize(f):
    """ Memoization decorator for functions taking one or more arguments. """
    class memodict(dict):
        def __init__(self, f):
            self.f = f
        def __call__(self, *args):
            return self[args]
        def __missing__(self, key):
            ret = self[key] = self.f(*key)
            return ret

    return memodict(f)


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
        req = self.session.get(url=url )
        soup = BeautifulSoup(req.content,
                                 parse_only=SoupStrainer('a', href=True))
    

        self.bs_links = soup.findAll('a', {'class': 'title'})
        #print(len(self.bs_links))        

    def __str__(self):
        return "Search"
    
    def __repr__(self):
        return self.__str__()

# get rid of this
meta_map = {
    'Installs': 'installs',
    ' Developer ': 'dev',
}

    
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
        self.dev = ''
        self.app_id = app_id
        self.description = ''
        self.installs = ''
        self.total_ratings = ''
        self.permissions = []
        self.rating = ''
        self.key_word = ''
        self.screenshots = []
        self.image = ''
        self.price = ''
        self.pub_date = ''
        self.genre = ''
        
        for key, value in kwargs.items():
            setattr(self, key, value)
        # preappending host
        self.url = 'https://play.google.com' + self.url

    def populate_fields(self):
        """Populate the apps fields. Sometimes this can
        take some time which is why you must call it when 
        you are ready.
        """
        self.get_permissions()
        self.populate_data()
        
        
    def get_permissions(self):
        """Get all the permissions for this app """
        # if the permissions are already set do not go fetch
        if self.permissions:
            return self.permissions

        # everything needs to be set inorder to get permissions
        if not self.app_id or not self.session.header_que or not self.session.cookie_que:
            raise Exception('You need proper app_id, headers, and cookie!')

        # log
        print('Requesting premissions from google')
    
        #url = 'https://play.google.com/store/getdevicepermissions?authuser=0'
        url = 'https://play.google.com/store/xhr/getdoc?authuser=0'
        # setting referer for header 
        ref = {'Referer':'https://play.google.com/store/apps/details?id='+self.app_id}

        # this can be removed
        cookies = self.session.cookie_que.copy()
        # preparing cooies
        requests.utils.add_dict_to_cookiejar(self.session.cookies, cookies)

        # add to header
        self.session.header_que.update(ref)
        # add to param
        self.session.param_que.update({'ids':str(self.app_id)})
        headers = self.session.header_que
        payload  = self.session.param_que

        # setting everything for post
        data = self.session.post(url=url,
                                 headers=headers,
                                 data=payload)

        # report status code
        print("Request complete, status code: " + str(data.status_code))
        _arr = data.content
        # convert javascript array into python list 
        _arr = _arr[6:].replace(",,", ",None,")
        _arr = _arr.replace(",, ", ",None,")
        _arr = _arr.replace(", ,", ",None,")
        _arr = _arr.replace(",,", ",None,")
        _arr = _arr.replace("[,", "[None,")
        _arr = _arr.replace('\r',' ').replace('\n',' ')
        _arr = _arr.replace('\\"', "\u0027")
        _app_array = ast.literal_eval(_arr)
    
        _app_obj = _app_array[0][2][0][55]
        # types of permissions ....
        stand_p = _app_obj[_app_obj.keys()[0]][1][0]
        other_p = _app_obj[_app_obj.keys()[0]][1][1]
        custom_p = _app_obj[_app_obj.keys()[0]][1][2]
        _permarr = []
        
        for a in stand_p:
            #print a
            for b in a[1]:
                 _permarr.append(b[0])
        for a in other_p:
            #print a
            for b in a[1]:
                 _permarr.append(b[0])
        for a in custom_p:
                 _permarr.append(a[0])
        
        
        # omg that worked
        # print json string from python object
        # print(json.dumps(_app_array, indent=4))
        self.permissions = _permarr
        return
        safe_content = data.content.decode('unicode-escape')

        _beg = str(safe_content).find('<div')
        _end = str(safe_content).rfind('</div>')

        safe_content = safe_content[(_beg-4):]
        safe_content = safe_content[:_end]

        soup = BeautifulSoup(safe_content)
        items = soup('div', {'class': 'perm-description'})
        # cleaning up permissions to be returned as array of str's
        self.permissions = [str(item.contents[0]) for item in items]

        return self.permissions

    def populate_data(self):
        """Helper to set the rest of the attributes of the this app
        """
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
                self.image = x.get('src')
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
        del app_dict['session']
        return app_dict
        

    def __str__(self):
        return "App"

    def __repr__(self):
        return self.__str__()

    
class PlayStore(Session):
    """Main wrapper for the google play store api. 
    The class is subclassing Session from requests.
    """
    
    def __init__ (self, cookie, token=''):
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
        

