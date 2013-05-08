# -*- coding: UTF-8 -*-
# 3/16/2012 5:30 PM

from __future__ import division
import urllib2, re, os, pickle, sys, csv
import codecs
from BeautifulSoup import BeautifulSoup, NavigableString, Tag
from urllib2 import Request, urlopen, URLError
import socket
from optparse import OptionParser
# import musicbrainzngs as m
import time
import gvm_tools
import Levenshtein as l

timeout = 10
socket.setdefaulttimeout(timeout)



def distance_calculator(a, a_mb):
    """
    Calculates the distance for two strings
    """
    nl_a = len(a)
    nl_a_mb = len(a)
    d_a = float((l.distance(a, a_mb))/(nl_a + nl_a_mb))
    return d_a

def rec_results_parser(tbody, rec_BDMC):
    """
    Returns the closest song name using Levenshtein ratio
    """
    
    tr = tbody.findAll('tr')
    # print tr
    rec_BDMC = unicode(rec_BDMC)
    
    print '\n', rec_BDMC
    
    ratios = []
    for i, entries in enumerate(tr[1:]):
        entry = entries.findAll('td')
        sco = entry[0].text
        rec = entry[1].text
        art = entry[3].text
        rel = entry[4].text
        
        if sco == str(100):
            ratio = l.jaro(rec_BDMC, rec)
            ratios.append(ratio)
            # print sco, '\t', rec, ratio, '\t', art, '\t', rel
    idx = ratios.index(max(ratios))
    return idx

def country_checker(art_mbid_url):
    """
    Checks country of a given MBID (most time for an artist name)
    """
    page_country = urllib2.urlopen(art_mbid_url)
    soup_country = BeautifulSoup(page_country)
    dt = soup_country.findAll('dt')
    for d in dt:
        if d.text == 'Country:':
            country = d.findNext().text
            return country

# TODO : try to do complete queries (as 'Yáñez' instead of Yaez)

def artist_MBID_checker(in_file, out_file):
    """
    Checks if an artist has a MBID on MB.
    """
    art_mbid_dict = {}
    input_file = open(in_file, 'rb')
    output_file = open(out_file, 'wb')
    error_log = open(''.join([out_file.split('.')[0], '_log.txt']), 'wb')
    error_log.write(gvm_tools.date_timestamp())
    error_log.write('\n')
    output_file.write('ARTIST\tQUERY\tMAX METRIC\tMETRIC 1\t\t\t\tMETRIC 2\t\t\t\tMETRIC 3\t\t\t\tMETRIC 4\t\t\t\tMETRIC 5\t\t\t\tMETRIC 6\n')

    reader = input_file.readlines()

    for j, line in enumerate(reader[1:]):

        line_split = line.decode('latin-1').split('\t')
        line_split = [ls.strip('\r\n') for ls in line_split]
        line_joined = []
        # print line_split
        
        art_orig = line_split[0]
        art = line_split[0].encode('ascii', 'asciify') # 0 for single-column artist, 1 for the full file
        # print art
        # art = re.sub(r'([+\-&|!(){}\[\]\^"~*?:\\])', r'', art)
        art_orig = re.sub(r'([+\&|!(){}\[\]\^"~*?:\\])', r'', art_orig)
        art = re.sub(r'([+\&|!(){}\[\]\^"~*?:\\])', r'', art)

        # print art
        art_q_orig = '+'.join(art_orig.split(' '))
        art_q = '+'.join(art.split(' '))
        
        url_query_orig = 'http://musicbrainz.org/search?query=%s+comment:Chile*+country:CL&type=artist&limit=10&advanced=1' %(art_q_orig)
        url_query = 'http://musicbrainz.org/search?query={0}+comment%3AChile*+country%3ACL&type=artist&limit=10&advanced=1'.format(art_q)
        
        
        # print j, '\t', art, '\t', url_query
        print j, '\t', art, '\t', url_query_orig
        

        if art_mbid_dict.get(art) is not None: # CHECKING IF THE ARTIST NAME IS ALREADY IN THE DICTIONARY
            art_mbid = art_mbid_dict.get(art)
            art_retrieved = art
        
        else:                                   # OR MAKING THE QUERY
            time.sleep(1)
            req = Request(url_query)
            try:
                # print 'A'
                response = urlopen(req)
            except URLError, e:
                # print 'EXCEPT'
                error_log.write(str(i))
                if hasattr(e, 'reason'):
                    print i, '\tWe failed to reach a server. Reason', e.reason
                elif hasattr(e, 'code'):
                    print 'The server couldn\'t fulfill the request. Error code: ', e.code    
            else:

                try:
                    # print 'B', url_query_orig.encode('UTF-8')
                    page = urllib2.urlopen(url_query_orig.encode('UTF-8'))
                    # print 'B1'
                    soup = BeautifulSoup(page)
                    # print 'B2'
                    tbody = soup.find('tbody')
                    # print 'B3'
                    tr = tbody.findAll('tr')
                    # print 'C'

                    distance_values = []
                    for i, entries in enumerate(tr[0:]):
                        # print 'D', i
                        
                        entry = entries.findAll('td')
                        # print entry
                        art_text = entry[1].text 
                        art_entry_orig = entries.find('a').text                       # artist name for printing
                        art_entry = entries.find('a').text              # artist name for the actual comparison
                        try:
                            art_entry_ascii = art_entry.encode('ascii', 'asciify')
                        except:
                            art_entry_ascii = art_entry
                        art_mbid = entry[1].find('a')['href']           # artist mbid link

                        # print unicode(art_orig), unicode(art_entry_orig)
                        ratio_orig_strings = l.ratio(unicode(art_orig), unicode(art_entry_orig))
                        jaro_orig_string = l.jaro(unicode(art_orig), unicode(art_entry_orig))
                        ratio_ascii_strings = l.ratio(unicode(art), unicode(art_entry_ascii)) # falta asciify art_entry
                        jaro_ascii_strings = l.jaro(unicode(art), unicode(art_entry_ascii))   # falta asciify art_entry
                        ratio_ascii_lower_no_spaces_strings = l.ratio(unicode(re.sub('( )', '', art).lower()), unicode(re.sub('( )', '', art_entry_ascii).lower())) # falta asciify art_entry
                        jaro_ascii_lower_no_spaces_strings = l.jaro(unicode(re.sub('( )', '', art).lower()), unicode(re.sub('( )', '', art_entry_ascii).lower())) # falta asciify art_entry


                        distance_values.append([ratio_orig_strings,                 # highest levenshtein ratio
                                                jaro_orig_string,                   # levenshtain lower-case no-space ratio
                                                ratio_ascii_strings,                # levenshtein jaro
                                                jaro_ascii_strings,                 # levenshtain lower-case no-space jaro
                                                ratio_ascii_lower_no_spaces_strings,# levenshtein jaro
                                                jaro_ascii_lower_no_spaces_strings, # levenshtain lower-case no-space jaro
                                                art_text, 
                                                art_entry, 
                                                art_mbid])#,                        

                    art_mbid_array = []
                    country_array = []
                    art_retrieved_array = []
                    metrics_array = []

                    for metric in xrange(6):

                        # metric_used = 4                                                         # ratio_ascii_lower_no_spaces_strings
                        max_value = [i[metric] for i in distance_values]                  
                        max_ratio_index = max_value.index(max(max_value))
                        metrics_array.append(distance_values[max_ratio_index][metric])


                        if distance_values[max_ratio_index][metric] >= 0.00:                 # Evaluate this value, it seems to be higher
                            art_mbid = distance_values[max_ratio_index][8]
                            country = str(country_checker(art_mbid))

                            # if country != 'None' and country != 'Chile':
                            #     art_mbid = 'WRONG COUNTRY'
                        else:
                            art_mbid = 'NO MATCH'
                            country = 'None'
                        
                        art_mbid_array.append(art_mbid)
                        country_array.append(country)
                        art_retrieved_array.append(distance_values[max_ratio_index][6])
                    # print art_mbid_array
                    # print country_array
                    # print 'XXX', art_retrieved_array
                    # art_retrieved = distance_values[max_ratio_index][6]#.encode('ascii', 'asciify')
                    art_mbid_dict[art] = art_mbid

                except:
                    error = ''.join([str(j), '\t', str(i), '\t', str(url_query), '\n'])
                    print error
                    error_log.write(str(error))

        try:
            # print art_retrieved, '\t', art_mbid, '\n'
            
            if len(line_split) == 1:                                            # If the file is only a list of artists
                # line_split.append(art_retrieved)
                line_split.append(url_query_orig)
                # line_split.insert(2, art_mbid)
                # line_split.append(country)
                line_split.append(str(1 + metrics_array.index(max(metrics_array)))) # IDX MAX METRIC VALUE

                for metric in xrange(6):
                    line_split.append(str(distance_values[max_ratio_index][metric]))
                    line_split.append(art_retrieved_array[metric])
                    line_split.append(art_mbid_array[metric])
                    line_split.append(country_array[metric])
                

                # line_split.append('\n')

            else:                                                               # If the file is a list of artists with the results
                line_split = [art,
                            art_retrieved,
                            art_mbid,
                            country,
                            str(distance_values[max_ratio_index][0]),
                            str(distance_values[max_ratio_index][1]),
                            str(distance_values[max_ratio_index][2]),
                            str(distance_values[max_ratio_index][3]),
                            str(distance_values[max_ratio_index][4]),
                            str(distance_values[max_ratio_index][5]),
                            url_query,
                            line_split[11]]
        
        except:
            error =  ''.join(['Error at ', str(j), '\n'])
            print error
            error_log.write(error)

        try:
            line_joined = '\t'.join(line_split).encode('latin-1')
            output_file.write(line_joined)
        except:
            line_joined = '\t'.join(line_split).encode('UTF-8')
            output_file.write(line_joined)
        
        output_file.write('\n')



    output_file.close()
    input_file.close()
    error_log.close()
    # return entries_dict



def mbid_writer(in_file, out_file):
    """
    Writes MBIDs for artist, release, and record, if they exist
    """

    input_file = open(in_file, 'rb')
    output_file = open(out_file, 'wb')
    output_log = ''.join([in_file.split('.')[0], '_log.txt'])
    error_log = open(output_log, 'wb')

    error_log.write(gvm_tools.date_timestamp())
    error_log.write('\n')

    reader = input_file.readlines()

    for i, line in enumerate(reader[1:]): # From first line since line 0 represent the keys

        line_split = line.decode('latin-1').split('\t')
        line_split = [ls.strip('\r\n') for ls in line_split]
        line_joined = []

        rec = line_split[0].encode('ascii', 'asciify')
        art = line_split[1].encode('ascii', 'asciify')
        rel = line_split[2].encode('ascii', 'asciify')

        # Escape Lucene's special characters.
        rec = re.sub(r'([+\-&|!(){}\[\]\^"~*?:\\])', r'', rec)
        art = re.sub(r'([+\-&|!(){}\[\]\^"~*?:\\])', r'', art)
        rel = re.sub(r'([+\-&|!(){}\[\]\^"~*?:\\])', r'', rel)

        rec_q = '%2B'.join(rec.split(' '))  # ' /'s changed by ',', splitted and joined for the query
        art_q = '%2B'.join(art.split(' '))
        rel_q = '%2B'.join(rel.split(' '))
     

        url_query = 'http://musicbrainz.org/search?query={0}+release%3A{1}+artist%3A{2}+comment%3AChile*+country%3ACL&type=recording&limit=25&advanced=1'.format(rec_q, rel_q, art_q)

        # print url_query

        # CHECKING IF THE SERVICE CAN BE ACCESSED
        time.sleep(1)
        req = Request(url_query)
        try:
            response = urlopen(req)
        except URLError, e:
            error_log.write(str(i))
            if hasattr(e, 'reason'):
                print i, '\tWe failed to reach a server. Reason', e.reason

            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request. Error code: ', e.code
        



        else:
            try:
                page = urllib2.urlopen(url_query)
                soup = BeautifulSoup(page)
                tbody = soup.find('tbody')

                idx = rec_results_parser(soup, rec) # retrieves the closest song index

                entry = tbody.findAll('tr')[idx]
                e = entry.findAll('td')
                rec_mb, rec_mbid = e[1].text, e[1].find('a')['href']
                art_mb, art_mbid = e[3].text, e[3].find('a')['href']
                rel_mb, rel_mbid = e[5].text, e[5].find('a')['href']

                
                # print art_mb, art_mbid
                # print rel_mb, rel_mbid


                ratio_art = l.jaro(unicode(art), unicode(art_mb))
                ratio_rec = l.jaro(unicode(rec), unicode(rec_mb))
                ratio_rel = l.jaro(unicode(rel), unicode(rel_mb))

                if ratio_art < 0.75:
                    art_mbid = ''
                    rec_mbid = ''
                    rel_mbid = ''
                else:
                    if ratio_rel < 0.75:
                        rel_mbid = ''
                        rec_mbid = ''
                    elif ratio_rec < 0.75:
                        rec_mbid = ''

                print str(i), rec_mb, art_mb, rel_mb, ratio_rec
                
                line_split.insert(1, rec_mbid)
                line_split.insert(3, art_mbid)
                line_split.insert(5, rel_mbid)
                line_split.insert(1, str(ratio_rec))
                line_split.append(url_query)

                line_split.append('\n')
                # print line_split

                line_joined = '\t'.join(line_split).encode('latin-1')

                output_file.write(line_joined)

                # print '\t'
                # print str(i)
                # print url_query   
                # print "%s\t%s\t%f\n %s\t%s\t%f\n %s\t%s\t%f" % (art, art_mb, ratio_art, rec, rec_mb, ratio_rec, rel, rel_mb, ratio_rel)     

            except:
                error = "{0}\t{1}\n".format(str(i), url_query)
                print error
                error_log.write(error)


    input_file.close()
    output_file.close()
    error_log.close()
            



#   De+tu+ausencia release:Polvo+de+estrellas artist:Alberto+Plaza comment:Chile* country:CL

if __name__ == "__main__":
    usage = "%prog input_file outout_file"
    opts = OptionParser(usage = usage)
    options, args = opts.parse_args()

    if not args:
        opts.error("You must supply arguments to this script.")  

    mbid_writer(args[0], args[1])
    print 'done'