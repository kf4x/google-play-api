__author__="javier"

import requests
from requests import Session
from requests.cookies import cookiejar_from_dict
from bs4 import BeautifulSoup, SoupStrainer
import pycurl

_URL = "https://play.google.com/store/getreviews"
_USER_AGENT = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
_ACCEPT = "*/*"
_ACCEPT_ENCODING = "gzip, deflate"
_ACCEPT_LANGUAGE = "en-US,en;q=0.8"
_CACHE_CONTROL = "no-cache"
_CONTENT_LENGTH = "129"
_CONTENT_TYPE = "application/x-www-form-urlencoded;charset=UTF-8"
_ORIGIN = "https://play.google.com"

# These are the cookies you need to supply
_COOKIE = {"SSID":"", "SID":"", "SAPISID":"", "PREF":"", "PLAY_PREFS":"", "PLAY_ACTIVE_ACCOUNT":"", "OGPC":"", "NID":"", "HSID":"", "APISID":"", "_gat":"", "_ga":""}


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
    """Search API- search the playstore for an app.
    """

    def __init__(self, session, key_word='',page=1):
        self.session = session
        
        if key_word is not None:
            self._search(key_word,page)
            
        
    def get_page(self):
        '''return all the apps from the given page'''
        apps = []
        for app in self.bs_links:
            index = app['href'].find('=')
            aid = app['href'][index+1:]
            apps.append(App(self.session, app_id=aid, url=app['href'], name=app['title']))
            
        return apps

    def _search(self, key_word, page=1):
        url= "https://play.google.com/store/search?q=" + key_word + "&c=apps" + "&start=" + str((page-1)*24) + "&num=24"
        
        req = self.session.get(url=url )
        soup = BeautifulSoup(req.content,
                                 parse_only=SoupStrainer('a', href=True))
    
        # print(len(bs_links))
        self.bs_links = soup.findAll('a', {'class': 'title'})
        return self.get_page()


    def __str__(self):
        return "SearchObj"
    
    def __repr__(self):
        return self.__str__()

meta_map = {
    'Installs': 'installs',
    ' Developer ': 'dev',
}

    
class App(object):
    """App as object
    """
    
    def __init__(self, session, **kwargs):
        self.session = session
        self.url = ''
        self.name = ''
        self.dev = ''
        self.app_id = ''
        self.description = ''
        self.installs = ''
        self.total_ratings = ''
        self.permissions = []
    
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.url = 'https://play.google.com' + self.url
        self._fill_data()

        
    def get_permissions(self):
        if self.permissions:
            return self.permissions

        if not self.app_id or not self.session.header_que or not self.session.cookie_que:
            raise Exception("You need proper app_id, headers, and cookie!")
        
        print('Requesting premissions from google')
    
        url = 'https://play.google.com/store/getdevicepermissions?authuser=0'
        ref = {'Referer':'https://play.google.com/store/apps/details?id='+self.app_id}
        
        
        cookies = self.session.cookie_que.copy()
        requests.utils.add_dict_to_cookiejar(self.session.cookies, cookies)
        # print(self.session.cookies)

        self.session.header_que.update(ref)
        self.session.param_que.update({'id':str(self.app_id)})
        headers = self.session.header_que
        payload  = self.session.param_que
        
        data = self.session.post(url=url,
                                 headers=headers,
                                 data=payload)
        
        safe_content = data.content.decode('unicode-escape')

        _beg = str(safe_content).find('<div')
        _end = str(safe_content).rfind('</div>')

        safe_content = safe_content[(_beg-4):]
        safe_content = safe_content[:_end]

        soup = BeautifulSoup(safe_content)
        items = soup('div', {'class': 'perm-description'})
        self.permissions = [str(item.contents[0]) for item in items]
        #return permissions
        return self.permissions

    def _fill_data(self):
        html = self.session.get(self.url)
        
        soup = BeautifulSoup(html.content.decode('unicode-escape'))
        self.description = soup('div', {'class': 'id-app-orig-desc'})[0].contents

        details_section = soup.find_all('div', {'class': 'meta-info'})
        # for every detail there is 1 div (wrapper) with 2 sub divs (title, content)
        
        for div in details_section:
            # using fild all to ensure type is preserved
            fnd = ''
            val = ''
            for child in div.find_all('div'):
                
                if 'title' in child.get('class'):
                    fnd = child.text
                if 'content' in child.get('class'):
                    val = child.text

            if fnd in meta_map:
                setattr(self, meta_map[fnd], val)
            
        
        
    def attrs(self):
        return self.__dict__

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class GoogleRequest(object):
    def __init__(self):
         # setting defaults 
        self.headers = {
            "accept", _ACCEPT, 
            "accept-encoding", _ACCEPT_ENCODING,
            "accept-language", _ACCEPT_LANGUAGE,
            "cache-connectiontrol", _CACHE_CONTROL,
            "connectiontent-length", _CONTENT_LENGTH,
            "content-type", _CONTENT_TYPE,
            "origin", _ORIGIN,
            "pragma", _CACHE_CONTROL,
            "user-agent", _USER_AGENT
        }

    
class PlayStore(Session):
    """ Interacting with the google play store
    you will need to supply:
        cookie
        token
    """
    def __init__ (self,token='', cookie={}):
        
        if token or cookie:
            self.set_creds(token=token, cookie=cookie)
        else:
            self.cookie_que = {}
            self.param_que = {}

        self.header_que = {
            "accept": _ACCEPT, 
            "accept-encoding": _ACCEPT_ENCODING,
            "accept-language": _ACCEPT_LANGUAGE,
            "cache-connectiontrol": _CACHE_CONTROL,
            "content-length": _CONTENT_LENGTH,
            "content-type": _CONTENT_TYPE,
            "origin": _ORIGIN,
            "pragma": _CACHE_CONTROL,
            "user-agent": _USER_AGENT
        }

        super(PlayStore, self).__init__()

    def set_creds(self, token='', cookie={}):
        check = set(_COOKIE.keys()).intersection(cookie.keys())
        if len(check) < len(_COOKIE.keys()) or token is None:
            print('Without token AND cookie data, search will not properly work.')
        

        # self.session.headers.update(self.header)
        self.cookie_que = cookie
        self.param_que = {
            'xhr': 1,
            'token': token,
            'id': ''
        }
        
    def search(self, kw, pg=1):
        """
        Returns a new search object
        """
        return Search(self, kw, pg)
        

    
