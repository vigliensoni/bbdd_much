import urllib2, re, os, pickle, sys, csv
from BeautifulSoup import BeautifulSoup
from optparse import OptionParser

sys.setrecursionlimit(10000)

class MyWriter: 
    def __init__(self, stdout, filename): 
        self.stdout = stdout 
        self.logfile = file(filename, 'a') 
    def write(self, text): 
        self.stdout.write(text) 
        self.logfile.write(text) 
    def close(self): 
        self.stdout.close() 
        self.logfile.close() 


def discography_from_musicapopular_cl(input_folder, output_folder):
    writer = MyWriter(sys.stdout, os.path.join(output_folder, '_log_test.txt'))
    sys.stdout = writer
    for dirpath, dirnames, filenames in os.walk(input_folder):
        for f in filenames:
            if f.startswith(".") or f.endswith(".txt"):
                continue
            file_path = os.path.join(dirpath, f)
            f = open(file_path, 'rb')
            page = pickle.load(f)

            disc = page.find('a', {'name':"discografia"})
            
            
            print disc.findAllNext()[0], disc.findAllNext()[1]


if __name__ == "__main__":
    usage = "%prog input_folder output_folder"# site_to_scrap?\n(1) musicapopular.cl\n(2) mus.cl\n(3)portaldisc.cl\n(4)vccl.tv"
    opts = OptionParser(usage = usage)
    options, args = opts.parse_args()

    if not args:
        opts.error("You must supply arguments to this script.")  

    discography_from_musicapopular_cl(args[0], args[1])
    # if args[1] == '1':
    #     print 'http://musicapopular.cl'
    #     musicapopular(args[0])
    # if args[1] == '2':
    #     print 'http://mus.cl'
    #     item_to_scrap = input('Please enter a value for (1) album_review, (2) interview or (3) concert_review\t')
    #     mus_cl(args[0], item_to_scrap) 
    # if args[1] == '3':
    #     print 'http://portaldisc.cl'
    #     portaldisc_cl(args[0])
    # if args[1] == '4':
    #     print 'http://vccl.tv'
    #     vccl_tv(args[0])