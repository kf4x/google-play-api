from gp import Search

# output file
FILENAME = "search.txt"

fpi = open(FILENAME, "a")   # append to file

# make a search object supplying the constructor with with term you want to search for
search = Search("twitter")


# there are 20 pages total for any search start from page 1
for page_num in range(1,20):
    out = ""
    # get apps on page x
    print "on page", page_num
    page = search.get_page(page=page_num)
    print "finished reading page", page_num
    #iterate through the apps on page x. there are 24 apps/page
    for app in range(0,24):
        # print page[app].get_name(), page[app].get_permission()
        out += "\n" + page[app].get_name() + " - " + str(page[app].get_permission())

    out += "\n"
    mystring = out.encode('ascii', 'ignore')
    fpi.write(mystring)
    print "finished writing page", page_num, "to", FILENAME

print "DONE!"
