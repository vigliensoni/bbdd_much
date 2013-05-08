import urllib2, re, os, pickle, sys, csv

from BeautifulSoup import BeautifulSoup, NavigableString, Tag
from optparse import OptionParser

sys.setrecursionlimit(10000)



def parser_genres(input_file):
    genres = []
    genre_counter = []
    i = open(input_file, 'rb')
    reader = i.readlines()
    for line in reader:
        splitted_line = line.split(',')
        for sp in splitted_line:
            if sp == '' or sp == '\r\n':
                pass
            g = re.sub('["\r\n]', '', sp).strip()
            try:    
                if genres.index(g):
                    pass
            except:
                genres.append(g)
            genre_counter.append(g)
    # print genre_counter
    print len(genres), genres
    for g in genres:
        print g, genre_counter.count(g)

    o = open('/Users/gabriel/Desktop/genre_counter', 'wb')
    for g in genres:
        full_line = "{0}\t{1}\n".format(g, genre_counter.count(g))
        o.write(full_line)

    o.close()

if __name__ == "__main__":
    usage = "%prog file"
    opts = OptionParser(usage = usage)
    options, args = opts.parse_args()

    if not args:
        opts.error("You must supply arguments to this script.")  

    parser_genres(args[0])
