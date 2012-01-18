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



def musicapopular(output_folder): #, item_to_scrap):

    writer = MyWriter(sys.stdout, os.path.join(output_folder, '_log_test.txt'))
    sys.stdout = writer

    def artist_review(idx):
        page = urllib2.urlopen("http://www.musicapopular.cl/3.0/index2.php?op=Artista&id={0}".format(idx))
        soup = BeautifulSoup(page)

        artist = soup.find('a', {'id':"up"})
        bio = soup.find('div', {'id':"colcentral_bio"})
        print ("{0}, {1}".format(i, artist.text.encode("utf-8")))
        return soup


    for i in xrange(30000):
        i += 1
        filename = os.path.join(output_folder, str(i))
        f = open(filename, 'w')
        soup = artist_review(i)
        pickle.dump(soup, f)     # TO DUMP IT AS PICKLE

    print 'END' 


def mus_cl(output_folder, item_to_scrap):

    writer = MyWriter(sys.stdout, os.path.join(output_folder, '_log_test.txt'))
    sys.stdout = writer

    def album_review(idx):
        page = urllib2.urlopen("http://mus.cl/discos_detalle.php?fId={0}".format(idx))
        soup = BeautifulSoup(page)
        artist = soup.find('span',{'class':"titulo"})
        album = soup.find('span',{'class':"parrafo"})
        try:
            print ("{0}, {1}, {2}".format(i, artist.text.encode("utf-8"), album.text.encode("utf-8")))
        except:
            print ("{0}, Null".format(i))
        return soup

    def interview(idx):
        page = urllib2.urlopen("http://mus.cl/entrevista.php?fId={0}".format(idx))
        soup = BeautifulSoup(page)
        artist = soup.find('span', {'class':"parrafo"})
        title = soup.find('span', {'class':"titulo_entrevista"})
        try:
            print ("{0}, {1}, {2}".format(i, artist.text.encode("utf-8"), title.text.encode("utf-8")))
        except:
            print ("{0}, Null".format(i))
        return soup

    def concert_review(idx):
        page = urllib2.urlopen("http://mus.cl/comentarios_detalle.php?fId={0}".format(idx))
        soup = BeautifulSoup(page)

        title = soup.find('span', {'class':"parrafo"})
        try :
            print ("{0}\t {1}".format(i, title.text.encode("utf-8")))
        except:
            print ("{0}\t Null".format(i))
        return soup


    for i in xrange(3000):
        i += 1
        filename = os.path.join(output_folder, str(i))
        f = open(filename, 'w')

        if item_to_scrap == 1:
            soup = album_review(i)
        elif item_to_scrap == 2:
            soup = interview(i)
        elif item_to_scrap == 3:
            soup = concert_review(i)

        pickle.dump(soup, f)     # TO DUMP IT AS PICKLE
        f.close()

    print 'END' 


def portaldisc_cl(output_folder):

    writer = MyWriter(sys.stdout, os.path.join(output_folder, '_log_test.txt'))
    sys.stdout = writer

    def artist_album(idx):
        page = urllib2.urlopen("http://portaldisc.cl/disco.php?id={0}".format(idx))
        soup = BeautifulSoup(page)
        artist_album = soup.find('span', {'class':"style1"})
        try:
            print ("{0}\t{1}\t{2}".format(idx, artist_album.contents[0].encode("utf-8"), artist_album.contents[2].strip().encode("utf-8")))
        except:
            print ("{0}\tNull".format(idx))

    for i in xrange(10000):
        i += 1
        filename = os.path.join(output_folder, str(i))
        f = open(filename, 'w')

        soup = artist_album(i)

        pickle.dump(soup, f)     # TO DUMP IT AS PICKLE
        f.close()

    print 'END'

def vccl_tv(output_folder):
    writer = MyWriter(sys.stdout, os.path.join(output_folder, '_log_test.txt'))
    sys.stdout = writer

    def videopages(idx):
        page = urllib2.urlopen("http://www.vccl.tv/wp2/archivo/videos/page/{0}/".format(idx))
        soup = BeautifulSoup(page)
        allvideolinks = soup.find('div', {'id':"nav-below"})
        videolinksperpage = allvideolinks.findNextSiblings()
        for c, video in enumerate(videolinksperpage[0:10]):
            filename = os.path.join(output_folder, str(idx)+str(c))
            f = open(filename, 'w')
            try:
                song_name = video.find('h2').text.encode("utf-8")
                artist_name = video.findAll('h3')[0].text.encode("utf-8")
                videolink = video.findAll('a')[0]['href']
                videopage = urllib2.urlopen(videolink)
                videosoup = BeautifulSoup(videopage)
                pickle.dump(videosoup, f)
                print ("{0}{4}\t{1}\t{2}\t{3}".format(idx, artist_name, song_name, videolink, c))
            except:
                print ("{0}{1}\tNull".format(idx, c))

    for i in xrange(10000):
        i += 1
        soup = videopages(i)

    print 'END'




if __name__ == "__main__":
    usage = "%prog output_dir site_to_scrap?\n(1) musicapopular.cl\n(2) mus.cl\n(3)portaldisc.cl\n(4)vccl.tv"
    opts = OptionParser(usage = usage)
    options, args = opts.parse_args()

    if not args:
        opts.error("You must supply arguments to this script.")  
    if args[1] == '1':
        print 'http://musicapopular.cl'
        musicapopular(args[0])
    if args[1] == '2':
        print 'http://mus.cl'
        item_to_scrap = input('Please enter a value for (1) album_review, (2) interview or (3) concert_review\t')
        mus_cl(args[0], item_to_scrap) 
    if args[1] == '3':
        print 'http://portaldisc.cl'
        portaldisc_cl(args[0])
    if args[1] == '4':
        print 'http://vccl.tv'
        vccl_tv(args[0])
    # if not args[0]:
    #     opts.error("You must supply an output directory.")
    # if not args[1]:
    #     opts.error("You must supply what do you want:\nalbum_review (1)\ninterview (2)\nconcert_review (3)) ")
    # if args[1] != 1 or 2 or 3:
    #     opts.error("second argument must be (1) for album_review, (2) for interview, or (3) for concert_review")


    # main(args[0])#, args[1])