from bs4 import BeautifulSoup
from pymarc import *
import requests
import webbrowser
import tkinter

root = tkinter.Tk()
root.withdraw()

# kanID = '1126650'
kanURL = 'https://www.kanopystreaming.com/s?query='
pdaSite = 'https://www.kanopystreaming.com/user/1198/pda-ng'
pdaKanopyMarcFile = 'C:\\Users\\fenichele\\Desktop\\pdaKanopyMarcFile.mrc'
licenseKanopyMarcFile = 'C:\\Users\\fenichele\\Desktop\\licenseKanopyMarcFile.mrc'

def loadCollections():
    collectionList = 'C:\\Users\\fenichele\\github\\KanopyCollection\\kanopy_pda_producers.txt'

    collections = []
    with open(collectionList, 'r') as x:
        collections = [line.strip() for line in x]

    return collections


def getKanHTML(kanID):
    kURL = kanURL
    kID = kanID

    kURLFull = kanURL+kanID
    print(kURLFull)

    r = requests.get(kURLFull)
    kHTML = r.text

    soup = BeautifulSoup(kHTML)

    return soup

def parseHTML(soup):

    coll = None
    for a in soup.find_all('div'):
        if a.has_key('class') and a['class'][0] == 'title':
            coll = a.text

    return coll

def testKanopy(kanopyID,titCollection):
    pdaCollections = loadCollections()

    collection = titCollection[titCollection.rfind('from')+5:len(titCollection)]
    title = titCollection[:titCollection.find('from')].strip()

    PDAgroup = None

    if collection in pdaCollections:
        PDAgroup = True
    elif collection == 'Media Education Foundation':
        PDAgroup = False
    else:
        webbrowser.open(kanURL+kanopyID, new=1)
        PDAgroupResponse = input('Is '+titCollection+' a PDA Title? \nTrue or False')
        if PDAgroupResponse in(True, 'true', 't', 'T'):
            PDAgroup = True
        else:
            PDAgroup = False

    return PDAgroup

def runKanopy(kanID):
    soup = getKanHTML(kanID)
    titCollection = parseHTML(soup)

    print(titCollection)
    collection = titCollection[titCollection.rfind('from')+5:len(titCollection)]
    title = titCollection[:titCollection.find('from')].strip()

    PDAGroup = testKanopy(kanID,titCollection)

    return PDAGroup

def writeToPDAFile(record, file):
    with open(file, 'ab') as x:
        try:
            x.write((record.as_marc()))
        except UnicodeEncodeError:
            print ("couldn't write")
    print("Written!")


def openKanopyMarc():
    marcFile = 'C:\\Users\\fenichele\\Desktop\\Kanopy_MARC_Records__fau.kanopystreaming.com__13-Mar-2015.mrc'

    from tkinter import  filedialog
    marcPath = tkinter.filedialog.askopenfile()
    marcFile = marcPath.name

    with open(marcFile, 'rb') as fh:
        reader = MARCReader(fh)

        for record in reader:
            lockanID = record['001'].value()
            lockanID = lockanID.strip('kan')

            isPDA = runKanopy(lockanID)
            print(lockanID, 'is pda:', isPDA)

            if isPDA is True:
                writeToPDAFile(record,pdaKanopyMarcFile)
            elif isPDA is False:
                writeToPDAFile(record,licenseKanopyMarcFile)
            else:
                "PDA is Unknown!"

            print('\n')


openKanopyMarc()