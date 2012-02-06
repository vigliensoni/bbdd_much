import urllib2, re, os, pickle, sys, csv

from BeautifulSoup import BeautifulSoup, NavigableString, Tag
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

    w = open('./listado_musica_popular.csv', 'wt')
    writer = csv.writer(w)


    def data_cleaner(array):
        '''Cleans '\n' and None in an array'''
        catenator = []
        for vector in array:
            while vector.count('\n') > 0:
                vector.remove('\n')
            while vector.count(None) > 0:
                vector.remove(None)
            catenator.append(''.join(vector))
        return catenator

    def instrument_parser(instruments):
        """Receives a string and parses it by 'y', and ','"""
        if len(instruments) < 1:
            return
        parsed_instruments = []
        instruments = re.split('[,y]', instruments)
        for i in instruments:
            instrument = i.strip().capitalize().encode('utf-8')
            # print i, instrument
            parsed_instruments.append(instrument)
        return parsed_instruments

    def years_parser(years):
        """Receives a string and parses it by 'y', and ','"""
        year_array = []
        if len(years) < 1:
            return
        eras = years.split(')')[0].split('/')
        for era in eras:
            parsed_years = []
            sp_years = re.split('([0-9]*)', era)
            for year in sp_years:
                if year.isdigit():
                    parsed_years.append(year)
            year_array.append(parsed_years)
        
        return year_array


    for dirpath, dirnames, filenames in os.walk(input_folder):
        for f in filenames:       
            if f.startswith(".") or f.endswith(".txt"):
                continue
            file_path = os.path.join(dirpath, f)
            g = open(file_path, 'rb')
            page = pickle.load(g)

            #ARTIST
            artist = page.find('a', {'id':"up"}).text

            #PEOPLE
            people = page.find('span', {'class':"boxficha_integrantes"})

            if not people: continue                        # FOR PAGES WITH NO DATA

            if people.findAll(text=True)[0].startswith('G'):   # For extracting groups for individuals
                artist_type = '1'
            elif people.findAll(text=True)[0].startswith('I'): # For extracting individuals from Groups
                artist_type = '2'       

            people_data = []
            for br in people.findAll('br')[0:-1]:
                data = []
                name = []
                alias = []
                instrument = []
                n = br.next
                while n == '\n': n = n.next
                while not (isinstance(n, Tag) and n.name == 'br'):  # While it is not a <br> tag

                    if n is None:                           # For handling None
                        print "ERROR: NONE"
                        break
                    if (isinstance(n,Tag)):
                        if n.name == 'em':                      # Alias with <em>
                            alias.append(n.text)
                        pass

                    elif (isinstance(n,NavigableString)):
                        # print n
                        o = re.sub('[\r\n]', '', n)             # Removes '\r' and '\n'
                        name.append(o)
                    n = n.next
                    # print name
                people_data.append(''.join(name))


            # people_data = data_cleaner(people_data)
            for pd in people_data: 
                person_row = []
                data = re.split('[,;] (.*) \(', pd)    # splitting everything ',' or ';' and '('
                name = data[0]
                # print name, data

                try:    instruments = data[1]
                except: instruments = []
                try:    years = data[2]
                except: years = []
    
                instruments = instrument_parser(instruments)
                years = years_parser(years)
                
                person_row.append(f)
                person_row.append(artist_type)
                person_row.append(artist.encode('utf-8'))
                person_row.append(name.encode('utf-8'))
                person_row.append(instruments)
                person_row.append(years)

                writer.writerow(person_row)

                print f,'\t',artist_type,'\t', artist,'\t', name, '\t', instruments, '\t', years#, 'http://www.musicapopular.cl/3.0/index2.php?op=Artista&id=&{0}'.format(f)


    w.close()



            # bio = page.find('div', {'id':"colcentral_bio"})
            # bio_creator = bio.find(text=re.compile("&mdash;")).split("&mdash;")[-1].lstrip(' ')
            
            # picture_creator = bio.find(text=re.compile("Foto:")).split("Foto:")[-1].lstrip(' ')

            # print '\n'


            
def ARTIST_from_musicapopular_cl(input_folder, output_folder):
    '''Parses artist_name, start_place, and begin_year for an specific artist in musicapopular_cl
    '''    
    # writer = MyWriter(sys.stdout, os.path.join(output_folder, '_log_test.txt'))
    # sys.stdout = writer
    for dirpath, dirnames, filenames in os.walk(input_folder):
        for f in filenames:
            # print f
            if f.startswith(".") or f.endswith(".txt"):
                continue
            

            file_path = os.path.join(dirpath, f)
            g = open(file_path, 'rb')
            page = pickle.load(g)


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
            
            
            print '\n'

if __name__ == "__main__":
    usage = "%prog input_folder output_folder"# site_to_scrap?\n(1) musicapopular.cl\n(2) mus.cl\n(3)portaldisc.cl\n(4)vccl.tv"
    opts = OptionParser(usage = usage)
    options, args = opts.parse_args()

    if not args:
        opts.error("You must supply arguments to this script.")  

    PEOPLE_ARTIST_from_musicapopular_cl(args[0], args[1])
    # ARTIST_from_musicapopular_cl(args[0], args[1])
    



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