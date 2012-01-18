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


def main(output_folder): #, item_to_scrap):

    writer = MyWriter(sys.stdout, os.path.join(output_folder, 'log_test.txt'))
    sys.stdout = writer

    def artist_review(idx):
        page = urllib2.urlopen("http://www.musicapopular.cl/3.0/index2.php?op=Artista&id={0}".format(idx))
        soup = BeautifulSoup(page)
    # try:
        artist = soup.find('a', {'id':"up"})
        bio = soup.find('div', {'id':"colcentral_bio"})
        print ("{0}, {1}".format(i, artist.text.encode("utf-8")))
        # time.sleep(1)
    # except:
        # print ("{0}, error or no more contents".format(i))
        return soup

    # def interview(idx):
    #     page = urllib2.urlopen("http://mus.cl/entrevista.php?fId={0}".format(idx))
    #     soup = BeautifulSoup(page)
    #     try:
    #         artist = soup.find('span', {'class':"parrafo"})
    #         title = soup.find('span', {'class':"titulo_entrevista"})
    #         print ("{0}, {1}, {2}".format(i, artist.contents, title.contents))
    #         # print artist, title
    #     except:
    #         print ("{0}, error or no more contents".format(i))
    #         # print
    #     return soup

    # def concert_review(idx):
    #     page = urllib2.urlopen("http://mus.cl/comentarios_detalle.php?fId={0}".format(idx))
    #     soup = BeautifulSoup(page)
    #     return soup



    for i in xrange(30000):
        i += 1
        filename = os.path.join(output_folder, str(i))
        f = open(filename, 'w')
        
        soup = artist_review(i)

        # if item_to_scrap == '1':
        #     soup = album_review(i)
            
        # elif item_to_scrap == '2':
        #     soup = interview(i)
        # elif item_to_scrap == '3':
        #     soup = concert_review(i)
        
    # try:
        pickle.dump(soup, f)     # TO DUMP IT AS PICKLE
    # except:
        # print 'error'
        # f.close()


        # pkl_file = open('data.pkl', 'rb')
        # data1 = pickle.load(pkl_file)

    print 'END' 



if __name__ == "__main__":
    usage = "%prog output_dir"# what_do_you_want_to_extract?\nalbum_review (1)\ninterview (2)\nconcert_review (3)"
    opts = OptionParser(usage = usage)
    options, args = opts.parse_args()


    if not args:
        opts.error("You must supply arguments to this script.")    
    # if not args[0]:
    #     opts.error("You must supply an output directory.")
    # if not args[1]:
    #     opts.error("You must supply what do you want:\nalbum_review (1)\ninterview (2)\nconcert_review (3)) ")
    # if args[1] != 1 or 2 or 3:
    #     opts.error("second argument must be (1) for album_review, (2) for interview, or (3) for concert_review")


    main(args[0])#, args[1])