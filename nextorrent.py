import os, sys, urllib, ConfigParser, shutil
from urlparse import urljoin

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

fp = webdriver.FirefoxProfile()

notYetOnline=[]

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

def moveToDownloads(file_extension,target):
    for file in os.listdir("."):
        if file.endswith(file_extension):
            shutil.move(file,target)

### TORRENT9
def getUrlFromTorrent9(episodeName):
    driver.get("https://www.nextorrent.net/")
    elem = driver.find_element_by_name("torrentSearch")
    elem.send_keys(episodeName)
    elem.send_keys(Keys.RETURN)

    try:
        wait = WebDriverWait(driver, 5)
        element= wait.until(EC.presence_of_element_located((By.XPATH,"html/body/div[5]/div[1]/div[2]/div/div/table/tbody/tr/td[1]/a[2]")))
    except:
        notYetOnline.append(ml)
        return 0

    return element.get_attribute("href")

def clickUrlTorrent9(url,name):
    driver.get(url)

    wait = WebDriverWait(driver, 5)
    element = wait.until(EC.presence_of_element_located((By.XPATH,"html/body/div[5]/div[1]/div[2]/div[1]/div[2]/div/div[2]/div[2]/a[1]")))
    link = element.get_attribute('href')
    url = urljoin(url, link)

    # download the torrent
    torrent = name+".torrent"
    print "-> "+torrent
    urllib.urlretrieve(url, torrent)
###

if __name__=="__main__":
    visible = ConfigSectionMap("SERIE")['visible']
    if (visible == "True"):
        driver = webdriver.Firefox(fp)
    elif (visible == "False"):
        driver = webdriver.PhantomJS()
    else:
        print ("ERROR DRIVER CONFIG")
        exit()

    try:
        with open("download.list","rb") as f:
            content = f.readlines()
        print "="*63+"\n"+"DOWNLOAD\n"+"="*63+"\n"
        for ml in content:
            ml = ml.rstrip('\n')
            if ("Lethal Weapon" in ml):
                ml = ml.replace("Lethal Weapon","L'Arme Fatale")
            if ("A Series of Unfortunate Events" in ml):
                ml = ml.replace("A Series of Unfortunate Events","Les desastreuses aventures des orphelins Baudelaire")
            url=getUrlFromTorrent9(ml)
            if (url != 0):
                clickUrlTorrent9(url,ml)
        moveToDownloads(".torrent", ConfigSectionMap("TORRENT")['download'])
        print "\n"+"="*63+"\n"+"NOT YET ON NEXTORRENT\n"+"="*63+"\n"
        for nyo in notYetOnline:
            print "-> "+nyo
        driver.quit()
    except:
        print ("ERROR NO download.list FILE")
        driver.quit()
