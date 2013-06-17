
from gp import Search

# make a search object supplying the constructor with with term you want to search for
search = Search("twitter")

# compare returns a Counter
counter = search.compare_page(1)

for k, v in counter.most_common(30):
    print '%s: %d' % (k, v)