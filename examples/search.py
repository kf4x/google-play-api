from gp import Search

# make a search object supplying the constructor with with term you want to search for
search = Search("twitter")

# get_first returns an App object
app = search.get_first()

# get the name  and permissions of the app
print app.get_name()
print app.get_permission()