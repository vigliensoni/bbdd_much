# -*- coding: utf-8 -*-
import urllib2, re, os, pickle, sys, csv
import codecs
import gvm_tools
from BeautifulSoup import BeautifulSoup, NavigableString, Tag
from optparse import OptionParser
import time, socket, operator
import Levenshtein as leven
from experiment import GT_keys

import musicbrainzngs as m
m.set_useragent("Chilean music database integration", "0.01", "http://sp.vigliensoni.com")

timeout = 10
socket.setdefaulttimeout(timeout)

def MBID_releases_iterator(mbid):
    """
    Returns a dictionary with all releases in the form {title:mbid} for a given artist MBID
    """
    releases = {}
    rel = m.browse_releases(mbid)['release-list']
    # print rel
    no_rel = len(rel)
    for i in xrange(no_rel):
        title = rel[i]['title']
        mbid_title = rel[i]['id']
        releases[title] = mbid_title
    # print releases
    return releases

def MBID_recording_iterator(mbid):
    """
    Returns a dictionary with all releases in the form {title:mbid} for a given artist MBID
    """
    recordings = {}
    recording_list = m.browse_recordings(release = mbid)['recording-list']
    no_rec = len(recording_list)
    for i in xrange(no_rec):
        title = recording_list[i]['title']
        mbid_title = recording_list[i]['id']
        recordings[title] = mbid_title
    # print recordings
    return recordings



def row_writer(row, mbid_artist, MBID_release):
    """
    Writes MBIDs for artists and releases
    """
    line = '\t'.join([row, mbid_artist, MBID_release])
    o_file.write(line)
    return

def MBID_retriever(i_file, o_file):
    """
    Receives a file with artist names, and assigns MBIDs from a ground truth values from a dictionary
    """
    i = 0
    prev_art = ''
    mbid_artist = ''
    mbid_release = ''
    mbid_recording = ''

    i_file = open(i_file, 'rb')
    o_file = open(o_file, 'wb')
    o_file.write('\n')
    mbid_keys = GT_keys('/Users/gabriel/Dropbox/1_PHD_VC/1_COURSES/1_MUMT609/8_DATA/EXPERIMENT/FINISHING_EXPERIMENT/800_artists.txt')
    reader = i_file.readlines()
    for line in reader[1:]:
        i += 1
        l_s = line.decode('latin-1').split('\t')
        title = l_s[0]
        artist = l_s[1]
        album = l_s[2]
        # print i, artist, album, title
        album_proc = album.encode('ascii', 'asciify')
        album_proc = gvm_tools.lowercase_nospace(album_proc)
        if artist == prev_art:
            pass
        elif artist in mbid_keys:
            mbid_artist = mbid_keys[artist].split('/')[-1]
            releases = MBID_releases_iterator(mbid_artist)
            album_distance = {}
            # Calculating Levenshtein distances for all possible albums
            for key_album in releases.iterkeys():
                key_ascii = key_album.encode('ascii', 'asciify')
                album_key_proc = gvm_tools.lowercase_nospace(key_ascii)
                lev_dist = leven.ratio(album_proc, album_key_proc)
                album_distance[key_album] = lev_dist
            # Only if an album was returned 
            if len(album_distance) > 0: 
                max_key = max(album_distance, key=album_distance.get)
                # Checking if the highest-distance is good enough
                if album_distance[max_key] > 0.75:
                    mbid_release = releases[max_key]
        else:
            mbid_artist = ''
            mbid_release = ''
            mbid_recording = ''

        # line_out = '\t'.join([line.strip(), mbid_artist, mbid_release, '\n'])
        # o_file.write(line_out)
        prev_art = artist
        # print mbid_artist, mbid_release
        
        # For the song comparison
        title_proc = title.encode('ascii', 'asciify')
        title_proc = gvm_tools.lowercase_nospace(title_proc)
        if mbid_release is not '':
            recording_list = MBID_recording_iterator(mbid_release)
            # print recording_list
            recording_distances = {}

            for recording_key in recording_list.iterkeys():
                recording_ascii = recording_key.encode('ascii', 'asciify')
                recording_proc = gvm_tools.lowercase_nospace(recording_ascii)
                recording_distance = leven.ratio(title_proc, recording_proc)
                recording_distances[recording_key] = recording_distance

                # print recording_key, recording_distance
            
            max_key = max(recording_distances, key=recording_distances.get)
            # print title, max_key, recording_distance, '\n'
            if recording_distances[max_key] > 0.75:
                mbid_recording = recording_list[max_key]
            else:
                mbid_recording = ''
            print i, artist, album, title, mbid_recording

        line_out = '\t'.join([line.strip(), mbid_artist, mbid_release, mbid_recording, '\n'])
        o_file.write(line_out)
        mbid_recording = ''

    print i
    o_file.close()
    i_file.close()
