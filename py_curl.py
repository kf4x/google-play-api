
import sys
import pycurl
import json
from BeautifulSoup import BeautifulSoup



class CBClass:
    x = 0
    def __init__(self):
        self.contents = ''

    def body_callback(self, buf):
        self.contents = self.contents + buf



t = CBClass()
c = pycurl.Curl()

c.setopt(c.URL, 'https://play.google.com/store/getdevicepermissions')

c.setopt(c.WRITEFUNCTION, t.body_callback)

c.setopt(c.HTTPHEADER, ['Cookie: PREF=ID=c696a2742cb72a8c:U=0dff6458d01a8cfc:FF=0:LD=en:TM=1375918333:LM=1375918708:S=wrEGpb7D1OTgSSGw; PLAY_PREFS=CgJVUxD7jYTZhSg:S:ANO1ljKp4n8fbXvp; NID=67=SVzphh8BjmJ4SrHU8mDsGqiWrAZYvQCP8y1OHJU5AvxS_aL1vtlSxeCY7PjvN05nuYKpC1E19RR7x_1pBdwKiC6wA2_nZrVheOAuUvC7OYojhKIZFejxCsZrxu7Yg8vvZntriX-7oFfdJPkEXzdDeQ5sCyajnilFkP0; SID=DQAAALwAAAAm5TOANcnCzV_K6z5ZtWWORBGWfi7CvJP9wOXPrnqpWBZUV0TdQZWNXr2WNnU7M4fhT5BEcP-Cgs1GAWdSJQ8eWqwgQ-8mLrs1VcKHZelFb7q_I0ZhsXeQ1tRL2wz5S7mR9dGG0TqnYB5LxXlm_eBdiZN_mUKjv8gq-Ykwyc9rxYiX_n06i0FeHDoxuA981j3_EdqxRTz_bK6QIaIjEFe_HMxo2dmgreIhQkMcT8X2rKaTfbkkw-s4au6GOPGcbfo; HSID=AcoTQHHYYN42Op8NL; SSID=APggUeOIfgSUN32Oz; APISID=ef4kvsQBkVFl8VM6/Am3Lk-MxdBSHQUgRc; SAPISID=x-zWa70_HEVoHIF3/A5HVApVB55u0DSr7f;PLAY_ACTIVE_ACCOUNT=ICrt_XL61NBE_S0rhk8RpG0k65e0XwQVdDlvB6kxiQ8=applidmail@gmail.com',
                        'Host: play.google.com',
                        'Referer: https://play.google.com/store/apps/details?id=com.twitter.android',
                        'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:23.0) Gecko/20100101 Firefox/23.0'])

c.setopt(c.POSTFIELDS, 'id=com.netflix.mediaclient&xhr=1&token=kGxukBkmCXTZFIG5Tk4fzMHBtsw%3A1375918986927')
c.setopt(c.POST, 1)
c.perform()
c.close()

mystring = t.contents.decode('unicode-escape')

_beg = str(mystring).find('<div')
_end = str(mystring).rfind('</div>')


mystring = mystring[_beg:]

mystring = mystring[:(len(mystring)-_end)+15]

soup = BeautifulSoup(mystring)
items = soup('div', {'class': 'perm-description'})


print([str(item.contents[0]) for item in items])

# card-content-link