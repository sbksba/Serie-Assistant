import datetime, sys, ConfigParser, ast, os, csv
from os import listdir
from os.path import isfile, join
import tmdbsimple as tmdb

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

Config = ConfigParser.ConfigParser()
Config.read("./config.ini")

tmdb.API_KEY = ConfigSectionMap("API")['key']

now = datetime.datetime.now().strftime('%Y-%m-%d')
print "DATE NOW : "+now
print "="*63+"\n"

def get_Serie_Id(serie_name):

    search = tmdb.Search()
    ser = search.tv(query=serie_name)
    for s in ser.get('results'):
        serie_id = s['id']
        break

    return serie_id

def get_Season_Number(serie_id):
    search = tmdb.TV(serie_id)
    ser = search.info()
    for s in ser.get("seasons"):
        if (s['season_number'] < 10):
            season_nb = "0"+str(s['season_number'])
        else:
            season_nb = str(s['season_number'])

    return season_nb

def get_Dict_Serie(mypath):
    if not os.path.exists(mypath):
        onlyfiles = []
    else:
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    key=1
    mydict = {}
    for f in onlyfiles:
        mydict [key] = f.rsplit('.',1)[0]
        key += 1

    return mydict

def print_tv(mypath,serie_name,target):
    status = 0
    name = serie_name.replace(" ","_").rsplit('.',1)[0]
    serie_id = get_Serie_Id(serie_name)
    season_nb = get_Season_Number(serie_id)

    mypath= mypath+name+"/S"+season_nb
    mydict = get_Dict_Serie(mypath)

    ## Get the episode to download (for a specific serie in argument)
    search = tmdb.TV_Seasons(serie_id,season_nb)
    ser = search.info()
    for s in ser.get('episodes'):
        if (s['episode_number'] < 10):
                episode = name+"_S"+season_nb+"E0"+str(s['episode_number'])
        else:
                episode = name+"_S"+season_nb+"E"+str(s['episode_number'])
        if (episode in mydict.values()):
            continue
        elif(now > s['air_date']):
            print "-> {:40} | {} | {:30} [DOWNLOAD]".format(s['name'].encode('utf-8'),s['air_date'],episode)
            target.write("{}\n".format(episode.replace("_"," ").rsplit('.',1)[0]))
            status = 1
    ##
    return status

mypath = ConfigSectionMap("SERIE")['path']
mylist = ast.literal_eval(Config.get("SERIE", "List"))
with open("download.list","w") as fcsv:
    for ls in mylist:
        print "-"*63
        print ls
        status = print_tv(mypath,ls,fcsv)
        if (status == 0):
            print "-> UP TO DATE"
