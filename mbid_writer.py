# -*- coding: UTF-8 -*-
import urllib2, re, os, pickle, sys, csv
import codecs
from BeautifulSoup import BeautifulSoup, NavigableString, Tag
from optparse import OptionParser
import musicbrainzngs as m
import time
import gvm_tools
m.set_useragent("Chilean music database integration", "0.01", "http://sp.vigliensoni.com")

def artist_mbid_find(artist_name):
    """
    Returns an artist MBID
    """
    artist_name = artist_name.decode('latin-1').encode('ascii', 'asciify')
    mb_artist_list = m.search_artists(artist_name)['artist-list'][0]
    mb_artist_name = mb_artist_list['name'].strip().encode('ascii', 'asciify')
    try: mb_artist_alias = mb_artist_list['alias-list']
    except: mb_artist_alias = ''
    mb_artist_id = mb_artist_list['id']

    
    if mb_artist_name and ((artist_name.lower() == mb_artist_name.lower()) or (artist_name in mb_artist_alias)):
        return mb_artist_id





def artist_mbid_writer(input_file, valid_artists, column):
    """
    If exist, writes MBIDs for Artist
    """
    out_file = open('./out_file.txt', 'wb')             # out_file
    orig_file = open(input_file, 'rb')                  # original_file with all_artists
    artist_file = open(valid_artists, 'rb')             # file with MBID valid artists (done with mbtester.artist_name_checker_mb())

    un_elem, all_elem = gvm_tools.unique_elements(input_file, int(column))  # unique elements of the input_file

    reader_orig_file = orig_file.readlines()
    reader_artist_file = artist_file.readlines()


    
    for artist in reader_artist_file:                        # iterating through lines in the validated artists file
        print artist
        
        a_mbid = artist_mbid_find(artist.strip())            # finds the MBID for each artist
        if a_mbid == None: a_mbid = ''

        rows = gvm_tools.rows_per_key(all_elem, artist.strip('\r\n'))    # finds all rows where that artist has a title in the original file
        for r in rows:                                      # iterating through the rows where artist has titles
            r += 1                                          # starting in 1st row
            o = reader_orig_file[r].split('\t')             

            o.insert(2, a_mbid)                             # inserting the artist MBID after artist name
            for i in o[:-1]: 
                out_file.write(''.join([i, '\t']))
            # out_file.write('\n')

    out_file.close()




    # reader = input_file.readlines()
    # for line in reader:
    #     mb_title = ''
    #     mb_artist = ''
    #     l = line.split('\t')
    #     title = l[0]
    #     artist = l[1]
    #     album = l[2]

    #     try: mb_title = m.search_recordings(title)['recording-list'][0]['title']
    #     except: pass
    #     try: mb_artist = m.search_recordings(title)['recording-list'][0]['artist-credit-phrase']
    #     except: pass

    #     print '{0}\t{1}\t{2}\n'.format(title, artist, album),
    #     print mb_title, '\t', mb_artist, '\n'



    # mb.get_release_by_id('22771713-f26f-41d5-9dc8-022ada190a98', includes = ['artists', 'labels', 'recordings'])['medium-list']



if __name__ == "__main__":
    usage = "%prog input_file file_with_valid_keys column_no_in_the_csv_file"
    opts = OptionParser(usage = usage)
    options, args = opts.parse_args()

    if not args:
        opts.error("You must supply arguments to this script.")  

    artist_mbid_writer(args[0], args[1], args[2])
    print 'done'