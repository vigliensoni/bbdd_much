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


def PEOPLE_ARTIST_from_musicapopular_cl(input_folder, output_folder):
    '''Parses f_name, l_name, instruments played, and active years of all people
    for an specific artist in musicapopular_cl
    '''
    # writer = MyWriter(sys.stdout, os.path.join(output_folder, '_log_test.txt'))
    # sys.stdout = writer
    for dirpath, dirnames, filenames in os.walk(input_folder):
        for f in filenames:
            print f
            if f.startswith(".") or f.endswith(".txt"):
                continue
            

            file_path = os.path.join(dirpath, f)
            f = open(file_path, 'rb')
            page = pickle.load(f)


            people = page.find('span', {'class':"boxficha_integrantes"}).text.split('.')

            for p in people:
                # print p
                if len(p) is not 0:
                    # PERSON
                    p = p.strip('Integrantes:')
                    name = p.split(',')[0].split()
                    f_name = [name[0]]
                    l_name = name[1:]
                    l_name = [' '.join(l_name)]

                    # INSTRUMENTS
                    instruments = []
                    init = p.find(',')
                    end = p.find('(')
                    instrument_list = p[init + 1:end]
                    instrument_list = instrument_list.replace(' y ', ',').split(',')
                    for i in instrument_list:
                        instruments.append(i.strip().capitalize())


                    # YEARS
                    init = [i for i, x in enumerate(p) if x == "("]
                    end = [i for i, x in enumerate(p) if x == ")"]
                    
                    try:
                        from_year = p[init[-1]]
                        to_year = p[end[-1]]

                        years = p[init[-1]+1:end[-1]]
                        years = years.split('-')
                        from_year = years[0].split()
                    except:
                        print 'error in years'
                    try:
                        to_year = years[1].split()
                    except:
                        to_year = from_year

                    print f_name, l_name, instruments, from_year, to_year



            bio = page.find('div', {'id':"colcentral_bio"})
            bio_creator = bio.find(text=re.compile("&mdash;")).split("&mdash;")[-1].lstrip(' ')
            
            picture_creator = bio.find(text=re.compile("Foto:")).split("Foto:")[-1].lstrip(' ')


            
def ARTIST_from_musicapopular_cl(input_folder, output_folder):
    '''Parses artist_name, start_place, and begin_year for an specific artist in musicapopular_cl
    '''    
    # writer = MyWriter(sys.stdout, os.path.join(output_folder, '_log_test.txt'))
    # sys.stdout = writer
    for dirpath, dirnames, filenames in os.walk(input_folder):
        for f in filenames:
            print f
            if f.startswith(".") or f.endswith(".txt"):
                continue
            

            file_path = os.path.join(dirpath, f)
            f = open(file_path, 'rb')
            page = pickle.load(f)


            #ARTIST
            artist = page.find('a', {'id':"up"}).text

            #FORMACION
            ficha = page.find('div', {'class':"boxficha"})
            ficha_data = ficha.find('p')
            begin_year = ficha_data.text.strip('Formaci&oacuten;:').split(',')[1].rstrip('.').strip()
            start_place = ficha_data.text.split(':')[1].split(',')[0].strip()

            #GENRE
            genre = []
            genres = ficha.findAll('p')[3].findChildren()
            for g in genres:
                genre.append(g.text)

            print artist, genre, start_place, begin_year
            
            


if __name__ == "__main__":
    usage = "%prog input_folder output_folder"# site_to_scrap?\n(1) musicapopular.cl\n(2) mus.cl\n(3)portaldisc.cl\n(4)vccl.tv"
    opts = OptionParser(usage = usage)
    options, args = opts.parse_args()

    if not args:
        opts.error("You must supply arguments to this script.")  

    # PEOPLE_ARTIST_from_musicapopular_cl(args[0], args[1])
    ARTIST_from_musicapopular_cl(args[0], args[1])
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