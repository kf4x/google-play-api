from gp import Search

# make a search object supplying the constructor with with term you want to search for
search = Search("twitter")


# page object with be returned. getting page 2
page = search.get_page(2)

#iterate through the apps on page 2. there are 24 apps/page
for app in range(0,24):
    print page[app].get_name(), page[app].get_permission()