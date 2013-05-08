# -*- coding: UTF-8 -*-
import urllib2, re, os, pickle, sys, csv
import codecs
from BeautifulSoup import BeautifulSoup, NavigableString, Tag
from optparse import OptionParser

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
            # ascii_entity = line_split[column].decode('latin-1').encode('ascii', 'asciify')
            # print line_split[column], ascii_entity
            # element_array.append(ascii_entity.strip())

            element_array.append(line_split[column].strip())

    return set(element_array), element_array


def name_merger(input_file_a, column_no_a, input_file_b, column_no_b):
    """Compares columns from two files and determines equal and different elements.
    Returns lists for both"""
    a_unique_list, a_list = unique_elements(input_file_a, int(column_no_a))
    b_unique_list, b_list = unique_elements(input_file_b, int(column_no_b))
    
    print "There are {0} same and {1} different artists in the two lists".format(len(a_unique_list.intersection(b_unique_list)), len(a_unique_list.symmetric_difference(b_unique_list)))
    return a_unique_list.intersection(b_unique_list), a_unique_list.symmetric_difference(b_unique_list)

if __name__ == "__main__":
    usage = "%prog input_file_a, column_no_a, input_file_b, column_no_b"
    opts = OptionParser(usage = usage)
    options, args = opts.parse_args()

    if not args:
        opts.error("You must supply arguments to this script.")  

    inter_list, diff_list = name_merger(args[0], args[1], args[2], args[3])

    out_int_file = open('./test_intersection.txt', 'wb')
    for f in inter_list:
        line = f + '\n'
        out_int_file.write(line)
    out_int_file.close()
    
    out_dif_file = open('./test_differences.txt', 'wb')
    for f in diff_list:
        line = f + '\n'
        out_dif_file.write(line)
    out_dif_file.close()


