import urllib2, re, os, pickle, sys, csv

from BeautifulSoup import BeautifulSoup, NavigableString, Tag
from optparse import OptionParser

sys.setrecursionlimit(10000)

# [0] muspop ID
# [1] soloist or band
# [2] artist_name
# [3] fname
# [4] lname
# [5] alias
# [6] instruments
# [7] years


def utf8_fixer(input_file, output_file):
    """Parses the instruments in the 'years' column to the instruments column"""
    i = open(input_file, 'rb')
    o = open(output_file, 'wb')
    reader = i.readlines()
    for line in reader:
        # fixed_line = re.sub('[a-z]', 'X', line)
        split_line = line.split(',')
        print split_line
        # MAKING The, Artist -> The Artist
        if split_line[1] == '1':
            split_line[3] = split_line[3] + ' ' + split_line[4]
            split_line[4] = ''
            # print split_line[2]

        # PARSING INSTRUMENTS ON lname TO instruments
        # if split_line[6] == 'None':
        #     # print split_line
        #     # print split_line[2], split_line[6],
        
        #     lname_array = split_line[4].split(',')
        #     split_line[4] = lname_array[0]
        #     split_line[6] = lname_array[1:]
        #     print split_line[6]
        

        # full_line = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}".format(split_line[0],split_line[1],split_line[2],split_line[3],split_line[4],split_line[5],split_line[6],split_line[7])
        # o.write(full_line)
    o.close()
    i.close()



if __name__ == "__main__":
    usage = "%prog input_file output_file"
    opts = OptionParser(usage = usage)
    options, args = opts.parse_args()

    if not args:
        opts.error("You must supply arguments to this script.")  

    utf8_fixer(args[0], args[1])
