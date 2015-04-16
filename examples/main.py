import googleplaystore
import json
cookie = {"PLAY_PREFS":"",
          "NID":"",
          "_gat":"",
          "_ga":""
          }

ps = googleplaystore.PlayStore(cookie=cookie)
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


