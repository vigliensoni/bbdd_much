# -*- coding: UTF-8 -*-
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

def rec_results_parser(xml, rec_BDMC):
    """
    Returns the entry song with the closest Levenshtein ratio
    """
    soup = BeautifulSoup(page)
    tbody = soup.find('tbody')
    tr = tbody.findAll('tr')
    for entries in tr:
        entry = entries.findAll('td')
        sco = entry[0].text
        rec = entry[1].text
        art = entry[3].text
        rel = entry[4].text
        if sco == str(100):
            print sco, '\t', rec, '\t', art, '\t', rel


    ratios = []
    for entries in tr:
        entry = entries.findAll('td')
        sco = entry[0].text
        rec = entry[1].text
        art = entry[3].text
        rel = entry[4].text
        if sco == str(100):
            ratio = l.ratio(rec_BDMC, rec)
            ratios.append(ratio)
            # print sco, '\t', rec, ratio, '\t', art, '\t', rel
    idx = ratios.index(max(ratios))
    return tr[idx]



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



        # print "REC:{0}\tART:{1}\tREL:{2}".format(rec, art, rel)

        rec_q = '%2B'.join(rec.split(' '))  # ' /'s changed by ',', splitted and joined for the query
        art_q = '%2B'.join(art.split(' '))
        rel_q = '%2B'.join(rel.split(' '))
        # print "ART:{0}\tREL:{1}\tREC:{2}".format(art, rel, rec)        

        url_query = 'http://musicbrainz.org/search?query={0}+release%3A{1}+artist%3A{2}+comment%3AChile*+country%3ACL&type=recording&limit=1&advanced=1'.format(rec_q, rel_q, art_q)



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
                resp = soup.findAll('tbody')[0].findAll('a')
                
                rec_mb, rec_mbid = resp[0].text, resp[0]['href']
                art_mb, art_mbid = resp[1].text, resp[1]['href']
                rel_mb, rel_mbid = resp[2].text, resp[2]['href']

                ratio_art = l.ratio(unicode(art), unicode(art_mb))
                ratio_rec = l.ratio(unicode(rec), unicode(rec_mb))
                ratio_rel = l.ratio(unicode(rel), unicode(rel_mb))

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

                line_split.insert(1, rec_mbid)
                line_split.insert(3, art_mbid)
                line_split.insert(5, rel_mbid)
                line_split.append(url_query)
                line_split.append('\n')
                # print line_split

                line_joined = '\t'.join(line_split).encode('latin-1')

                output_file.write(line_joined)

                # print '\t'
                print str(i)
                print url_query   
                print "%s\t%s\t%f\n %s\t%s\t%f\n %s\t%s\t%f" % (art, art_mb, ratio_art, rec, rec_mb, ratio_rec, rel, rel_mb, ratio_rel)     

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