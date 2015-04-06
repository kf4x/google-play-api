import googleplaystore
import json
cookie = {"SSID":"",
          "SID":"",
          "SAPISID":""
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
# get a single app
app = all_apps[0]

# show the string representation of the app
print app

# print all the permissions
print json.dumps(app.get_permissions(), indent=3)

# print app as dictionary
print app.to_dict()


