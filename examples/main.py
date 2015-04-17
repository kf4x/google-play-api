import googleplaystore
import json
cookie = {"PLAY_PREFS":"",
          "NID":"",
          "_gat":"",
          "_ga":""
          }

ps = googleplaystore.PlayStore(cookie=cookie)
#returns a search object
search_obj = ps.search()
# return an array of Apps
all_apps = search_obj.search('twitter')
# get a single app and get all its data
app = all_apps[0].populate_fields()

# show the string representation of the app
print app

# print all the permissions
print json.dumps(app.to_dict(), indent=3)

# print app as dictionary
print app.to_dict()


