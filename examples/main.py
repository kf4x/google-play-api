import googleplaystore
import json
cookie = {"SSID":"",
          "SID":"",
          "SAPISID":"/AID7mn_K4ezijGt0X"
          "PREF":"",
          "PLAY_PREFS":"",
          "PLAY_ACTIVE_ACCOUNT":"",
          "NID":"",
          "HSID":"",
          "APISID":"",
          "_gat":"",
          "_ga":""
          }

token = ''
ps = googleplaystore.PlayStore(cookie=cookie, token=token)
#returns a search object
search = ps.search('twitter')
# return an array of Apps
all_apps = search.get_page()

twi = all_apps[0]
print twi

#print all the permissions
print json.dumps(twi.get_permissions(), indent=3)

# print app as dictionary
print twi.attrs()


