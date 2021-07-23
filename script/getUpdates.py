# ==========================================================
# ==========================================================

# Das script sucht nach einem neuen "daily"
# und meldet, wenn es eines findet und das gefundene
# "daily" aktueller ist, als das aktuell verwendete
# Programm.
#
# Es kann nach "dailys" der Programme:
# MTPlayer und P2Radio
# gesucht werden.
#
# Dem Script kann man die eigene Einstellung des
# Config-Ordners mitgeben, auch kann man angeben
# nach welchen "dailys" gesucht werden soll.


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

# Hier kann man auswählen, nach welchem "daily" gesucht
# werden soll.
# True   ->  es wird danach gesucht
# False  ->  es wird nicht danach gesucht

searchMtplayer = True
searchP2radio  = True



# ==========================================================
# ==========================================================
import xml.etree.ElementTree as ET
import sys, urllib.request
import platform
from datetime import datetime
from pathlib import Path
home = str(Path.home())
os = platform.system()
urlMtplayer = "https://www.p2tools.de/mtplayer/download.html"
urlP2Radio = "https://www.p2tools.de/p2radio/download.html"


if pathMtplayer == "":
    if os=="Windows":
        #Windows
        configMtplayer = home + "\\p2Mtplayer\\mtplayer.xml"

    else:
        #Linux
        configMtplayer = home + "/.p2Mtplayer/mtplayer.xml"

else:
    configMtplayer = pathMtplayer

if pathP2radio == "":
    if os=="Windows":
        #Windows
        configP2radio = home + "\\p2Radio\\p2radio.xml"

    else:
        #Linux
        configP2radio = home + "/.p2Radio/p2radio.xml"

else:
    configP2radio = pathP2radio
    

def dailyDate(url):
    search1='<a href="/daily/'.encode()
    search2='__'.encode()
    search3='.zip'.encode()
    try:
        u=urllib.request.urlopen(url)
    except:
        print("Fehler: Kann die Website nicht finden")
        sys.exit(0)

    li = u.readlines()
    u.close
    ts = ""
    for line in li:
        pos1 = line.find(search1)
        pos2 = pos1 + len(search1)
        pos2 = line.find(search2, pos2) + len(search2)
        pos3 = line.find(search3, pos2)
        
        if pos1 != -1:
            ts = line[pos2:pos3]
            d =  ts.decode('utf-8')
            date = datetime.strptime(d, '%Y.%m.%d')

    return date


def getXmlBuildDate(file, tag):
    xmlFile = Path(file)
    if not xmlFile.is_file():
        print("Fehler: Config-File: " + file)
        print("Fehler: Config-File konnte nicht gefunden werden")
        sys.exit(0)

    tree = ET.parse(file)
    root = tree.getroot()
    for element in root.findall(tag):
        bDate = element.find('system-prog-build-date')
        if bDate is None:
            print("Fehler: Config-File: " + file)
            print("Fehler: BuildDate konnte im Config-File nicht gefunden werden")
            sys.exit(0)

        buildDate = bDate.text
        date = datetime.strptime(buildDate, '%d.%m.%Y')

    return date


if searchMtplayer:
    print()
    print("------------------------")
    print("======  MTPlayer  ======")
    print("------------------------")
    dXml = getXmlBuildDate(configMtplayer, 'system')
    dD = dailyDate(urlMtplayer)
    if dXml < dD:
        print("Es gibt   ===> EIN <===    aktuelleres daily")
        print("BuildDate Programm: ", datetime.strftime(dXml, '%d.%m.%Y'))
        print("BuildDate daily:    ", datetime.strftime(dD, '%d.%m.%Y'))
    else:
        print("Es gibt   ===> KEIN <===   aktuelleres daily")
        print("BuildDate Programm: ", datetime.strftime(dXml, '%d.%m.%Y'))
        print("BuildDate daily:    ", datetime.strftime(dD, '%d.%m.%Y'))
    print()
    print()
    

if searchP2radio:
    print()
    print("-----------------------")
    print("======  P2Radio  ======")
    print("-----------------------")
    dXml = getXmlBuildDate(configP2radio, 'ProgConfig')
    dD = dailyDate(urlP2Radio)
    if dXml < dD:
        print("Es gibt   ===> EIN <===   aktuelleres daily")
        print("BuildDate Programm: ", datetime.strftime(dXml, '%d.%m.%Y'))
        print("BuildDate daily:    ", datetime.strftime(dD, '%d.%m.%Y'))
    else:
        print("Es gibt   ===> KEIN <===   aktuelleres daily")
        print("BuildDate Programm: ", datetime.strftime(dXml, '%d.%m.%Y'))
        print("BuildDate daily:    ", datetime.strftime(dD, '%d.%m.%Y'))


print()
print()
print("-----------------------------------------------------")
print("download dailys: ", "https://www.p2tools.de/daily/")
print("-----------------------------------------------------")

