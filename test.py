from BeautifulSoup import BeautifulSoup
import urllib
import re
import requests
import codecs
import unidecode
import binascii
import json


from xml.sax.saxutils import escape, unescape


page=urllib.urlopen("https://play.google.com/store/search?q=facebook&c=apps")
soup = BeautifulSoup(page.read())
inner = soup('script')
# print str(inner[11].string) 



match = re.findall(r'(?<=\{)(.*?)(?=\})', inner[11].string)
for m in match:
    # print type(m)
    # print urllib.unquote(m)
    # print codecs.decode(m, "string_escape")
    print m
    print'============================'
