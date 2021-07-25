#!/usr/bin/python
#-*- coding:utf-8 -*-

scriptBuildDate = "23.07.2021"


# ==========================================================
# ==========================================================
# Das script sucht nach
# neuen Infos
#
# einer aktuelleren Programmversion
# einer neuen beta-Version
# einem neuen daily-build
#
# und meldet, wenn es eines findet und das gefundene
# aktueller ist, als das aktuell verwendete Programm.
#
# Es kann nach updates der Programme:
# MTPlayer und P2Radio
# gesucht werden.
#
# Dem Script kann man die eigene Einstellung des
# Config-Ordners mitgeben, auch kann man angeben
# nach welchen Programmen gesucht werden soll.


# ==========================================================
# ==========================================================
# Hier kann man den Pfad zum Config-Ordner angeben.
# Wird der Standard-Ordner verwendet, braucht nichts
# angegeben werden.

# Standardpfad bei Linux
#pathMtplayer = "/home/USER/.p2Mtplayer/mtplayer.xml"
#pathP2radio = "/home/USER/.p2Radio/p2radio.xml"

# Standardpfad bei Windows
#pathMtplayer = "C:\Users\USER\p2Mtplayer\mtplayer.xml"
#pathP2radio = "C:\Users\USER\p2Radio\p2radio.xml"

pathMtplayer = ""
pathP2radio = ""


# ==========================================================
# ==========================================================
# Hier kann man auswählen, nach welchem Programm gesucht
# werden soll.
# True   ->  es wird danach gesucht
# False  ->  es wird nicht danach gesucht

searchMtplayer   = True
searchP2Radio    = True
searchGetUpdate  = True



# ==========================================================
# ==========================================================
import xml.etree.ElementTree as ET
import sys, urllib.request
import platform
from datetime import datetime
from pathlib import Path

home = str(Path.home())
os = platform.system()
urlFindUpdate = "https://www.p2tools.de/download/"
#urlFindUpdate = "http://p2.localhost:8080/download/"


def getUrl(url):
    try:
        lines = urllib.request.urlopen(url).readlines()
    except:
        print("Fehler: Kann die Website nicht finden")
        sys.exit(0)

    return lines


def getDate(lines, searchUrl, searchSuffix):
    #<p><a href="/download/p2radio/beta/P2Radio-1-32__2021.06.16.zip">P2Radio-1-32__2021.06.16.zip</a></p>
    #<p><a href="/download/mtplayer/act/MTPlayer-10__Linux+Java__2021.02.19.zip">MTPlayer-10__Linux+Java__2021.02.19.zip</a></p>
    #<p><a href="/download/p2radio/info/P2Radio__2021.07.20_1.txt">P2Radio__2021.07.20_1.txt</a></p>
    search1 = searchUrl.encode()
    search2 = '__'.encode()
    search3 = searchSuffix.encode()
    search4 = '_'.encode()

    ts = ""
    foundDate = datetime.strptime("1970.01.01", '%Y.%m.%d')
    for line in lines:
        pos1 = line.find(search1)
        pos2 = pos1 + len(search1)
        pos2 = line.rfind(search2, pos2) + len(search2)
        pos3 = line.find(search3, pos2)
        
        if pos1 != -1:
            ts = line[pos2:pos3]
            
            pos4 = ts.find(search4)
            if pos4 != -1:
                ts = ts[0:pos4]
            
            d =  ts.decode('utf-8')
            foundDate = datetime.strptime(d, '%Y.%m.%d')

    return foundDate


def getXmlBuildDate(file, tag, dateTag):
    xmlFile = Path(file)
    if not xmlFile.is_file():
        print("Fehler: Config-File: " + file)
        print("Fehler: Config-File konnte nicht gefunden werden")
        sys.exit(0)

    tree = ET.parse(file)
    root = tree.getroot()
    for element in root.findall(tag):
        bDate = element.find(dateTag)
        if bDate is None:
            print("Fehler: Config-File: " + file)
            print("Fehler: BuildDate konnte im Config-File nicht gefunden werden: " + dateTag)
            buildDate = "01.01.1970"
        else:
            buildDate = bDate.text
 
    foundDate = datetime.strptime(buildDate, '%d.%m.%Y')
    return foundDate


def searchData(progName, progPath, configPath, configTag):
    print()
    print("===================================")
    print(progName)
    print("-----------------------------------")
      
    #Infos
    startDate = datetime.strptime("01.01.1970", '%d.%m.%Y')
    dD = getDate(allLines, '<a href="/download/' + progPath + '/info/' + progName, ".txt")
    if startDate < dD:
        print("  Infos:  ===>  INFOS vorhanden")
        print("    InfoDate: ", datetime.strftime(dD, '%d.%m.%Y'))
    else:
        print("  Infos:  keine INFOS")
    print()

    #act
    dateConfig = getXmlBuildDate(configPath, configTag, 'system-prog-build-date')
    dD = getDate(allLines, 'href="/download/' + progPath + '/act/' + progName, ".zip")
    if dateConfig < dD:
        print("  Programm  ==>  AKTUELLERE VERSION vorhanden")
        print("    BuildDate Programm: ", datetime.strftime(dateConfig, '%d.%m.%Y'))
        print("    BuildDate act:      ", datetime.strftime(dD, '%d.%m.%Y'))
    else:
        print("  Es gibt keine aktuellere VERSION")
        print("    BuildDate Programm: ", datetime.strftime(dateConfig, '%d.%m.%Y'))
        print("    BuildDate act:      ", datetime.strftime(dD, '%d.%m.%Y'))
    print()

    #beta
    dD = getDate(allLines, 'href="/download/' + progPath + '/beta/' + progName, ".zip")
    if dateConfig < dD:
        print("  beta  ==>  AKTUELLERES BETA vorhanden")
        print("    BuildDate Programm: ", datetime.strftime(dateConfig, '%d.%m.%Y'))
        print("    BuildDate beta:     ", datetime.strftime(dD, '%d.%m.%Y'))
    else:
        print("  Es gibt keine aktuellere BETA")
        print("    BuildDate Programm: ", datetime.strftime(dateConfig, '%d.%m.%Y'))
        print("    BuildDate beta:     ", datetime.strftime(dD, '%d.%m.%Y'))
    print()

    #daily
    dD = getDate(allLines, 'href="/download/' + progPath + '/daily/' + progName, ".zip")
    if dateConfig < dD:
        print("  daily  ==>  AKTUELLERES DAILY vorhanden")
        print("    BuildDate Programm: ", datetime.strftime(dateConfig, '%d.%m.%Y'))
        print("    BuildDate daily:    ", datetime.strftime(dD, '%d.%m.%Y'))
    else:
        print("  Es gibt kein aktuelleres DAILY")
        print("    BuildDate Programm: ", datetime.strftime(dateConfig, '%d.%m.%Y'))
        print("    BuildDate daily:    ", datetime.strftime(dD, '%d.%m.%Y'))
    print("-----------------------------------")
    print()
    print()


def searchGetUpdateData():
    #<p><a href="/download/getUpdate/GetUpdates__2021.07.24.py">GetUpdates__2021.07.24.py</a></p>
    print()
    print("===================================")
    print("GetUpdate")
    print("-----------------------------------")

    date = datetime.strptime(scriptBuildDate, '%d.%m.%Y')
    dateWeb = getDate(allLines, '<a href="/download/getUpdate/GetUpdates', ".py")
    if date < dateWeb:
        print("  GetUpdate  ==>  AKTUELLERES GETUPDATE vorhanden")
        print("    BuildDate Programm: ", datetime.strftime(date, '%d.%m.%Y'))
        print("    BuildDate act:      ", datetime.strftime(dateWeb, '%d.%m.%Y'))
    else:
        print("  Es gibt kein aktuelleres GETUPDATE")
        print("    BuildDate Programm: ", datetime.strftime(date, '%d.%m.%Y'))
        print("    BuildDate act:      ", datetime.strftime(dateWeb, '%d.%m.%Y'))
    print()
    print("-----------------------------------")
    print()
    print()


#=========================================
#los gehts
#=========================================
if pathMtplayer == "":
    if os=="Windows":
        configMtplayer = home + "\\p2Mtplayer\\mtplayer.xml"
    else: #Linux
        configMtplayer = home + "/.p2Mtplayer/mtplayer.xml"
else:
    configMtplayer = pathMtplayer


if pathP2radio == "":
    if os=="Windows":
        configP2radio = home + "\\p2Radio\\p2radio.xml"
    else: #Linux
        configP2radio = home + "/.p2Radio/p2radio.xml"
else:
    configP2radio = pathP2radio
    

allLines = getUrl(urlFindUpdate)
        
#== MTPlayer Infos suchen
if searchMtplayer:
    searchData("MTPlayer", "mtplayer", configMtplayer, 'system')
 
    
#== P2Radio Infos suchen
if searchP2Radio:
    searchData("P2Radio", "p2radio", configP2radio, 'ProgConfig')

#== GetUpdate Infos suchen
if searchGetUpdate:
    searchGetUpdateData()


print()
print("-----------------------------------------------------")
print("download Updates:  ", "https://www.p2tools.de/download/")
print("-----------------------------------------------------")

