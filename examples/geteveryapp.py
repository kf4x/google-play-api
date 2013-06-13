from gp import Search

fpi = open("search.txt","w")   #write to file


# make a search object supplying the constructor with with term you want to search for
search = Search("twitter")

out = ""
# there are 20 pages total for any search
for page_num in range(0,20):
    # get apps on page x
    page = search.get_page(page=page_num)
    #iterate through the apps on page x. there are 24 apps/page
    for app in range(0,24):
        # print page[app].get_name(), page[app].get_permission()
        out += page[app].get_name(), page[app].get_permission()

    out += "\n"


fpi.write(out)
