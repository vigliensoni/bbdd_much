# -*- coding: utf-8 -*-
import urllib2, re, os, pickle, sys, csv
import codecs
import datetime

# from BeautifulSoup import BeautifulSoup, NavigableString, Tag
# from optparse import OptionParser
# import musicbrainzngs as m
# import time

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
u"č": u"c", u"ç": u"c", u"è": u"e", u"é": u"e", u"ê": u"e", u"ë": u"e",
u"ì": u"i", u"í": u"i", u"î": u"i", u"ï": u"i", u"ð": u"d",
u"ñ": u"n", u"ò": u"o", u"ó": u"o", u"ô": u"o", u"õ": u"o",
u"ö": u"o", u"÷": u"/", u"ø": u"o", u"ù": u"u", u"ú": u"u",
u"û": u"u", u"ü": u"u", u"ý": u"y", u"þ": u"p", u"ÿ": u"y", 
u"’": u"", u"“": u"", u"”": u"", u'"': u"", u"\x93": u"", 
u"\x94": u"", u"\u0414": u"e", u"\xb0": u"o", u"ő": u"o", u'\u2026':u""}#, u"\xe1":u""}



def asciify(error):
    return map[error.object[error.start]], error.end
codecs.register_error('asciify', asciify)

def date_timestamp():
    """
    Returns a string with the date in the form yyyy/mm/dd
    """
    o = datetime.datetime.now().timetuple()
    return '/'.join([str(o.tm_year), str(o.tm_mon), str(o.tm_mday)])


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

def rows_per_key(all_elem, key):#, column_album, column_songs):
    """
    Returns all rows where a specific key, in a specific row, is.
    First value is the key
    """
    e = ([i for i, x in enumerate(all_elem) if x == key])
    # e.insert(0, key)
    return e

def date_parser(date):
    """
    It parses a date with the form '06 de enero de 1971' and returns (6, 1, 1971)
    """
    day = ''
    month = ''
    year = ''
    months = {'enero':1,
            'febrero':2, 
            'marzo':3, 
            'abril':4, 
            'mayo':5, 
            'junio':6, 
            'julio':7, 
            'agosto':8, 
            'septiembre':9, 
            'octubre':10, 
            'noviembre':11, 
            'diciembre':12}

    elements = [e.strip(' ') for e in date.split('de')]
    for e in elements:
        e = re.sub(r'([\-,.?X])', r'', e).strip(' ')
        if e.isdigit() is True and len(e)<=2:
            day = str(e)
        elif e.isalpha() is True and len(e)>=4:
            month_st = str(e)
            month = str(months[month_st])
        elif e.isdigit() is True and len(e)>=4:
            year = str(e)

    return day, month, year

def colours(n):
    """
    It returns a colour name from a numberf for matplotlib plots
    """
    c = {0:'blue', 
        1:'green',
        2:'red',
        3:'cyan',
        4:'magenta',
        5:'black',
        6:'yellow',
        7:'white'}
    return c[n]


def matrix_transposition(A):
    """
    Transposes and returns a matrix_transposition
    """

    cols = len(A[0])
    # print cols
    T = [[row[i] for row in A] for i in range (cols)] # TRANSPOSING THE MATRIX A
    return T


def lowercase_nospace(string):
    """
    Returns a lower-cased, no-space, asciified version of a string
    """
    # string = string.decode('UTF-8')
    # No-space
    string = re.sub(r' ', '', string)
    # lower-case
    string = string.lower()
    return string
    



