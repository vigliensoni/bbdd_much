# -*- coding: UTF-8 -*-
import urllib2, re, os, pickle, sys, csv
import codecs
from BeautifulSoup import BeautifulSoup, NavigableString, Tag
from optparse import OptionParser
import musicbrainzngs as m
import time
m.set_useragent("Chilean music database integration", "0.01", "http://sp.vigliensoni.com")


map = {
u"¡": u"!", u"¢": u"c", u"£": u"L", u"¤": u"o", u"¥": u"Y",
u"¦": u"|", u"§": u"S", u"¨": u"`", u"©": u"c", u"ª": u"a",
u"«": u"<<", u"¬": u"-", u"­": u"-", u"®": u"R", u"¯": u"-",
u"°": u"o", u"±": u"+-", u"²": u"2", u"³": u"3", u"´": u"'",
u"µ": u"u", u"¶": u"P", u"·": u".", u"¸": u",", u"¹": u"1",
u"º": u"o", u"»": u">>", u"¼": u"1/4", u"½": u"1/2", u"¾": u"3/4",
u"¿": u"?", u"À": u"A", u"Á": u"A", u"Â": u"A", u"Ã": u"A",
u"Ä": u"A", u"Å": u"A", u"Æ": u"Ae", u"Ç": u"C", u"È": u"E",
u"É": u"E", u"Ê": u"E", u"Ë": u"E", u"Ì": u"I", u"Í": u"I",
u"Î": u"I", u"Ï": u"I", u"Ð": u"D", u"Ñ": u"N", u"Ò": u"O",
u"Ó": u"O", u"Ô": u"O", u"Õ": u"O", u"Ö": u"O", u"×": u"*",
u"Ø": u"O", u"Ù": u"U", u"Ú": u"U", u"Û": u"U", u"Ü": u"U",
u"Ý": u"Y", u"Þ": u"p", u"ß": u"b", u"à": u"a", u"á": u"a",
u"â": u"a", u"ã": u"a", u"ä": u"a", u"å": u"a", u"æ": u"ae",
u"ç": u"c", u"è": u"e", u"é": u"e", u"ê": u"e", u"ë": u"e",
u"ì": u"i", u"í": u"i", u"î": u"i", u"ï": u"i", u"ð": u"d",
u"ñ": u"n", u"ò": u"o", u"ó": u"o", u"ô": u"o", u"õ": u"o",
u"ö": u"o", u"÷": u"/", u"ø": u"o", u"ù": u"u", u"ú": u"u",
u"û": u"u", u"ü": u"u", u"ý": u"y", u"þ": u"p", u"ÿ": u"y", 
u"’": u"'", u"“": u"'", u"”": u"'", u'"': u"'", u"\x93": u"'", 
u"\x94": u"'"}

def asciify(error):
    return map[error.object[error.start]], error.end
codecs.register_error('asciify', asciify)


def unique_elements(input_file, column):
    """Receives a list and returns a list with the unique entries, and a list with the whole set"""
    input_file = open(input_file, 'rb')
    element_array = []
    reader = input_file.readlines()
    for line in reader[1:]:
        line_split = line.split('\t')
        if line_split[column] != '':
            element_array.append(line_split[column].strip())
    input_file.close()
    return list(set(element_array)), element_array




def bdmc_retriever(input_file, column_no):
    """Receives an input file formatted as a table, and a column number.
    Returns two lists, one with the unique entries, and other with all elements"""



    column_label = {'0':'Title', 
                    '1':'Artist', 
                    '2':'Album', '3':'Track', 
                    '4':'Year', 
                    '5':'Length', 
                    '6':'Size', '7':'Last Modified', '8':'Path', '9':'Filename', '10':'MP3 IdTag', 
                    '11':'Artista del album', 
                    '12':'Numero de disco', 
                    '13':'Género', 
                    '14':'Sello', 
                    '15':'Compositor', 
                    '16':'Codificado por', '17':'BPM', '18':'Codec', '19':'Bitrate', '20':'Frecuencia', '21':'VBR', '22':'Modo', '23':'Size', '24':'Modificado'}
    file_name = 'out_' + column_label[column_no] + '.txt'
    
    out_write = open(file_name, 'wb')

    un_elem, all_elem = unique_elements(input_file, int(column_no))
 
    writer = 'From a total of {0} entries, there are {1} different {2}s\n'.format(len(all_elem), len(un_elem), column_label[column_no])
    print writer
    out_write.write(writer)

    for el in un_elem:
        writer = "{0}\t{1}\n".format(el, all_elem.count(el))
        out_write.write(writer)

    out_write.close()
    return


def artist_name_checker_mb(input_file, column_no):
    """
    Checks if the name of a BDMC artist is on MB. Returns
    on_MB list 
    non_MB list
    """
    on_MB = []
    non_MB = []

    un_elem, all_elem = unique_elements(input_file, int(column_no))

    for j, artist in enumerate(un_elem[0:]):
        print j
        artist_mb_name = ''
        artist_mb_name_ascii = ''
        artist_mb_type = ''
        artist_mb_country = ''
        artist_mb_alias = ''
        time.sleep(1)                       # musicbrainz TOS

        artist_dec = artist.decode('latin-1')
        artist_ascii = artist_dec.encode('ascii', 'asciify')

        try: artist_mb = m.search_artists(artist_dec)['artist-list'][0]
        except: artist_mb = ''
        try: artist_mb_name = artist_mb['name']
        except: pass
        try: artist_mb_name_ascii = artist_mb_name.encode('ascii', 'asciify')
        except: artist_mb_name_ascii = ''
        try: artist_mb_type = artist_mb['type']
        except: pass
        try: artist_mb_country = artist_mb['country']
        except: pass
        try: artist_mb_alias = artist_mb['alias-list']
        except: artist_mb_alias = ''
        

        if artist_mb_name and ((artist_ascii.upper() == artist_mb_name_ascii.upper()) or (artist_ascii in artist_mb_alias)):
            on_MB.append(artist)

        else:
            non_MB.append(artist)

    return on_MB, non_MB


def album_song_checker_mb(input_file, column_artist):#, column_album, column_songs):
    """
    Checks if an artist album is on MB, but only among artists in MB
    """

    un_elem, all_elem = unique_elements(input_file, int(column_artist))
    input_file = open(input_file, 'rb')

    # I HAVE TO TAKE THE LIST OF ALREADY VALIDATED ARTISTS IN BOTH DATABASES

    for u_a in un_elem:         # unique_artists
        # print u_a, [i for i, x in enumerate(all_elem) if x == u_a]
        e = ([i for i, x in enumerate(all_elem) if x == u_a])
        e.insert(0, u_a)
        print e






# def mbid_artist_writer(input_file, on_MB):
#     """
#     Writes MBIDs for artists on BDMC
#     """
#     input_file = open(input_file, 'rb')
#     reader = input_file.readlines()
#     for line in reader:
#         rows = album_song_checker_mb(line)



if __name__ == "__main__":
    usage = "%prog [BDMC_RETRIEVER(1), ARTIST_NAME_CHECKER_MB(2), or ALBUM_SONG_CHECKER_MB(3), input_file, column_no"
    opts = OptionParser(usage = usage)
    options, args = opts.parse_args()

    if not args:
        opts.error("You must supply arguments to this script.")  

    if args[0] == '1':
        bdmc_retriever(args[1], args[2])
    elif args[0] == '2':
        on_MB, non_MB = artist_name_checker_mb(args[1], args[2])
        out_correct = open('./artists_on_MB_and_table.txt', 'wb')
        out_wrong = open('./artists_not_on_MB_and_table.txt', 'wb')

        out_correct.write('Existant chilean artists on MusicBrainz with the EXACT spelling of the table\n')
        out_wrong.write('Non-existant chilean artists on MusicBrainz with the EXACT spelling of the table\n')

        for a in on_MB:
            out_correct.write(a)
            out_correct.write('\n')
        out_correct.close()

        # mbid_writer(args[1], on_MB)

        for a in non_MB:
            out_wrong.write(a)
            out_wrong.write('\n')
        out_wrong.close()

    elif args[0] == '3':
        album_song_checker_mb(args[1], args[2])   
    else:
        print 'Choose (1) for BDMC_RETRIEVER, (2) for ARTIST_NAME_CHECKER_MB, or (3) FOR ALBUM_SONG_CHECKER_MB'



    



# ## ['recording-list']
# {'artist-credit': [{'artist': {'sort-name': 'Cholomandinga', 'id': '94d68b21-18a3-43e9-8e83-e7382c173f1c', 'name': 'Cholomandinga'}}], 
# 'length': '312000', 
# 'release-list': [{'status': 'Official', 
#                 'title': 'Porque Chile es Porno', 
#                 'date': '2000', 
#                 'country': 'CL', 
#                 'release-group': {'type': 'Album'}, 
#                 'id': '22771713-f26f-41d5-9dc8-022ada190a98', 
#                 'medium-list': [{}, {'position': '1', 'track-list': [{'title': 'El opio del pueblo'}], 
#                 'format': 'CD'}]}], 
# 'title': 'El opio del pueblo', 
# 'puid-list': ['9f220577-95f9-3b48-cce5-ff69fa74c7a3'], 
# 'id': '5ceaf33c-0503-4905-8028-5d34fd7ebce7', 
# 'artist-credit-phrase': 'Cholomandinga'}



    # print m.get_artist_by_id("952a4205-023d-4235-897c-6fdb6f58dfaa", [])
    # print m.get_label_by_id("aab2e720-bdd2-4565-afc2-460743585f16")
    # print m.get_release_by_id("e94757ff-2655-4690-b369-4012beba6114")
    # print m.get_release_group_by_id("9377d65d-ffd5-35d6-b64d-43f86ef9188d")
    # print m.get_recording_by_id("cb4d4d70-930c-4d1a-a157-776de18be66a")
    # print m.get_work_by_id("7e48685c-72dd-3a8b-9274-4777efb2aa75")

    # print m.get_releases_by_discid("BG.iuI50.qn1DOBAWIk8fUYoeHM-")
    # print m.get_recordings_by_puid("070359fc-8219-e62b-7bfd-5a01e742b490")
    # print m.get_recordings_by_isrc("GBAYE9300106")
    # print m.get_artist_by_name("Radiohead", [])

    # m.auth("", "")
    #m.submit_barcodes({"e94757ff-2655-4690-b369-4012beba6114": "9421021463277"})
    #m.submit_puids({"cb4d4d70-930c-4d1a-a157-776de18be66a":"e94757ff-2655-4690-b369-4012beba6114"})
    #m.submit_tags(recording_tags={"cb4d4d70-930c-4d1a-a157-776de18be66a":["these", "are", "my", "tags"]})
    #m.submit_tags(artist_tags={"952a4205-023d-4235-897c-6fdb6f58dfaa":["NZ", "twee"]})

    #m.submit_ratings(recording_ratings={"cb4d4d70-930c-4d1a-a157-776de18be66a":20})

    #print m.get_recordings_by_echoprint("aryw4bx1187b98dde8")
    #m.submit_echoprints({"e97f805a-ab48-4c52-855e-07049142113d": "anechoprint1234567"})
    


