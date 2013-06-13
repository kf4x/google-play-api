# this is just a module with helpers


import urllib2


def getHTML(url):
    return urllib2.urlopen(url).read()


def makeQuery(q, p):
    return "https://play.google.com/store/search?q=" + q + "&c=apps" + "&start=" + str((p-1)*24) +"&num=24"

