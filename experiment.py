# -*- coding: UTF-8 -*-
from __future__ import division
import random
from optparse import OptionParser
import re, time, pickle, sys, csv, os, socket, urllib2
from urllib2 import Request, urlopen, URLError
import codecs
from BeautifulSoup import BeautifulSoup, NavigableString, Tag
from optparse import OptionParser
import gvm_tools
import Levenshtein as l

import pylab
import numpy
import matplotlib.pyplot as plot
from matplotlib import rc
rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)

timeout = 10
socket.setdefaulttimeout(timeout)


def random_samples(i_file, o_file, sample_population_size):
    """
    Returns a file with a random population size after some 
    filtering ('Chile' or 'None', and ratios lesser than 1.0)
    """
    i_file = open(i_file, 'rb')
    o_file = open(o_file, 'wb')
    reader = i_file.readlines()
    sel_entries = []

    for i, line in enumerate(reader[1:3144]):
        l = line.split('\t')
        # if l[3] == 'Chile' or l[3] == 'None':
        print [e for e in l], '\n'
        if 0.75 <= float(l[4]) <= 1.0 and 0.75 <= float(l[8]) <= 1.0 and 0.75 <= float(l[12]) <= 1.0 and 0.75 <= float(l[16]) <= 1.0 and 0.75 <= float(l[20]) <= 1.0 and 0.75 <= float(l[24]) <= 1.0:
            sel_entries.append(line)
    print i, len(sel_entries)

    random_entries = random.sample(sel_entries, int(sample_population_size))
    for r in random_entries:
        o_file.write(r)

    o_file.close()
    i_file.close()
    return

def GT_keys(i_file):
    """
    Receives an input file and parse key, values if a certain condition is met
    """
    # print 'XXX'
    mbid_keys = {}
    i_file = open(i_file, 'rb')
    reader = i_file.readlines()
    for line in reader[1:]:
        l_s = line.split('\t')
        art = l_s[1]    # 0 
        mbid = l_s[6]   # 2
        res = l_s[7]   # 11
        if res == '1':
            mbid_keys[art] = mbid
    i_file.close()
    return mbid_keys

def GT_comparison(gt_file, i_file, o_file):
    """
    Receives a ground truth file and an input file.... 
    """
    mbid_keys = GT_keys(gt_file)
    # print mbid_keys
    i_file = open(i_file, 'rb')
    o_file = open(o_file, 'wb')
    reader = i_file.readlines()
    for line in reader[1:]:
        l_s = line.split('\t')
        id_no = l_s[0]
        art = l_s[1]
        metr_a = [l_s[4], l_s[8], l_s[12], l_s[16], l_s[20], l_s[24]]
        mbid_a = [l_s[6], l_s[10], l_s[14], l_s[18], l_s[22], l_s[22]]


        if mbid_keys.has_key(art):              # If the artist is in the GT
            o_file.write(line)
    o_file.close()
    i_file.close()
            


def prec_recall(i_file, o_file, case, choose_print=None):
    """
    Calculates precision and recall for the two cases. Also print the results.
    """

    i_file = open(i_file, 'rb')
    o_file = open(o_file, 'wb')
    reader = i_file.readlines()

    precision = []
    recall = []
    f_score = []

    for metric_no in xrange(6):
        p = []                         # single precision (one metric)
        r = []                          # single recall (one metric)
        f_s = []                       
        for t in xrange(75, 101): 
            th = t/100.0                # threshold [0.75, 1.00]
            tp = []
            fn = []
            fp = []

            for line in reader[1:]:
                # print line
                ls = line.split('\t')
                mt_vl = float(ls[4 + metric_no * 5])    # metric value
                gt = ls[7 + metric_no * 5]              # ground truth result ('1', '2' or '3')


                if case == 1:
                    if mt_vl >= th:
                        if gt == '1': tp.append(gt)
                        elif gt == '2' or gt =='3' : fp.append(gt)
                    elif mt_vl < th:
                        if gt == '1': fn.append(gt)

                elif case == 2:
                    if mt_vl >= th:
                        if gt == '1' or gt == '2': tp.append(gt)
                        elif gt == '3': fp.append(gt)    
                    elif mt_vl < th:
                        if gt == '1' or gt == '2': fn.append(gt)
                else: print "Case should be of type 1 or 2"  

            n_tp = len(tp)
            n_fn = len(fn)
            n_fp = len(fp)
            # print 'TH:{0}\tNo_TP:{1}\tNo_FN:{2}\tNo_FP:{3}'.format(th, n_tp, n_fn, n_fp)

            pr = n_tp / (n_tp + n_fp + 0.01)   # precision
            rc = n_tp / (n_tp + n_fn + 0.01)   # recall

            fs = 2*pr*rc/(pr+rc)

            p.append(pr)
            r.append(rc)
            f_s.append(fs)

        # print "Precision:{0}\nRecall:{1}".format(p, r)
        
        precision.append(p)
        recall.append(r)
        f_score.append(f_s)

    # print "Precision:{0}\nRecall:{1}".format(precision, recall)   

    # PLOTTING

    metrics_names = {0:'R', 
                    1:'J', 
                    2:'AR', 
                    3:'AJ', 
                    4:'NSLAR', 
                    5:'NSLAJ'}

    if choose_print:
        if case == 1:
            plot.figure(1, figsize = (10, 6.25))
            plot.title('Precision and recall of six methods for the true positives')
            plot.xlabel('Threshold', fontsize = 12)
            plot.ylabel('Normalized precision', fontsize = 12)

            for metric_no in xrange(6):
                t = numpy.arange(0.75, 1.01, 0.01)
                plot.plot(t, precision[metric_no], label = metrics_names[metric_no], color = gvm_tools.colours(metric_no))
                plot.plot(t, recall[metric_no], color = gvm_tools.colours(metric_no))
                plot.plot(t, f_score[metric_no], color = gvm_tools.colours(metric_no)) 
                
        elif case == 2:
            plot.figure(1, figsize = (10, 6.25))
            plot.title('Precision and recall of six methods for the true positives (and 2s considered as True)')
            plot.xlabel('Threshold', fontsize = 12)
            plot.ylabel('Normalized precision', fontsize = 12)

            for metric_no in xrange(6):
                t = numpy.arange(0.75, 1.01, 0.01)
                plot.plot(t, precision[metric_no], label = metrics_names[metric_no], color = gvm_tools.colours(metric_no)) 
                plot.plot(t, recall[metric_no], color = gvm_tools.colours(metric_no))
                plot.plot(t, f_score[metric_no], color = gvm_tools.colours(metric_no)) 

        pylab.ylim([0.4, 1.0])
        pylab.xlim([0.75, 1.0])
        plot.legend(loc='lower right')
        plot.grid()
        plot.show()
    elif not choose_print:
        i_file.close()
        o_file.close()
        # print "Precision:{0}\nRecall:{1}".format(precision, recall)
        return precision, recall


def thousand_files(i_file, o_folder, no_files, choose_range):
    """
    Returns thousand different populations without replacement from a unique one.
    Intended for bootstraping.

    Example:tf('/Users/gabriel/Dropbox/1_PHD_VC/1_COURSES/1_MUMT609/8_DATA/EXPERIMENT/Ground_Truth/GT_all800.txt', 
                '/Users/gabriel/Documents/5_DATASETS/2_MUMT609/1000_populations', 1000, 800)
    """
    i_file = open(i_file, 'rb')
    reader = i_file.readlines()

    for i in xrange(1, no_files + 1):
        filename = '%04d.txt' % (i)
        fullpath = os.path.join(o_folder, filename)
        o_file = open(fullpath, 'wb')
        o_file.write(reader[0])
        for x in xrange(1, choose_range + 1):
            o_file.write(random.choice(reader[1:]))
        o_file.close()
    i_file.close()
            

def precision_and_recall_1000_files(input_dir, o_file):
    """
    """
    # case = 1 # FOR ONLY 1s CONSIDERED AS TRUE POSITIVES
    case = 2 # FOR 1s AND 2s CONSIDERED AS TRUE POSITIVES
    o_file = open(o_file, 'wb')
    for dirpath, dirname, filenames in os.walk(input_dir):
        for f in filenames:
            if f.split('.')[-1] == 'txt':
                filepath =  os.path.join(input_dir, f)
                print filepath
                precision_array = []
                recall_array = []
                precision, recall = prec_recall(filepath, '/Users/gabriel/Documents/5_DATASETS/2_MUMT609/fake.txt', case)
                for prec in precision:
                    for p in prec:
                        precision_array.append(p)  
                line_precision = '\t'.join(str(p) for p in precision_array)
                for rec in recall:
                    for r in rec:
                        recall_array.append(r)
                line_recall = '\t'.join(str(p) for p in recall_array)
                line = '\t'.join([line_precision, line_recall])

                o_file.write(line)
                o_file.write('\n')
                # print "{0}\t{1}\t{2}".format(f, precision, recall)
                # i_file = open(f, 'rb')
                # i_file.close()


    o_file.close()

def discarding_5_percent(i_file, o_file):
    """
    """

    i_file = open(i_file, 'rb')
    o_file = open(o_file, 'wb')

    reader = i_file.readlines()
    A = []
    for line in reader:
        # print line
        
        a = []
        l_s = line.split('\t')
        for l in l_s:
            a.append(l.strip('\r\n'))
        A.append(a)

    T = gvm_tools.matrix_transposition(A)
    # print T
    no_instances = 25
    for row in T:
        print row
        for i in xrange(no_instances):
            row.remove(max(row))
        for i in xrange(no_instances):
            row.remove(min(row)) 
    A = gvm_tools.matrix_transposition(T)
    # print A

    for row in A:
        line = '\t'.join(str(r) for r in row)
        # print line
        o_file.write(line)
        o_file.write('\n')

    o_file.close()
    i_file.close()


# def MBID_assign(i_file, o_file):
#     """
#     Receives a file with artist names, and assigns MBIDs from a ground truth values from a dictionary
#     """
#     i = 0
#     prev_art = ''

#     i_file = open(i_file, 'rb')
#     o_file = open(o_file, 'wb')
#     mbid_keys = GT_keys('/Users/gabriel/Dropbox/1_PHD_VC/1_COURSES/1_MUMT609/8_DATA/EXPERIMENT/FINISHING_EXPERIMENT/800_artists.txt')
#     reader = i_file.readlines()
#     for line in reader[1:]:
#         l_s = line.split('\t')
#         tit = l_s[0]
#         art = l_s[1]
#         alb = l_s[2]
#         if art in mbid_keys:
#             i += 1
#             print art, mbid_keys[art]
            

#     print i
#     o_file.close()
#     i_file.close()








if __name__ == "__main__":
    usage = "%prog input_file output_file sample_population_size"# output_file sample_population_size"
    opts = OptionParser(usage = usage)
    options, args = opts.parse_args()

    if not args:
        opts.error("You must supply arguments to this script.")  


    

    
    print 'done'