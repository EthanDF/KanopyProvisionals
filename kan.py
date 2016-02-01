from bs4 import BeautifulSoup
from pymarc import *
import requests
import webbrowser
import tkinter

root = tkinter.Tk()
root.withdraw()

# kanID = '1126650'
kanURL = 'http://fau.kanopystreaming.com/node/'
pdaSite = 'https://www.kanopystreaming.com/user/1198/pda-ng'
pdaKanopyMarcFile = 'C:\\Users\\fenichele\\Desktop\\pdaKanopyMarcFile.mrc'
licenseKanopyMarcFile = 'C:\\Users\\fenichele\\Desktop\\licenseKanopyMarcFile.mrc'

def loadCollections():
    collectionList = 'kanopy_pda_producers.txt'

    collections = []
    with open(collectionList, 'r') as x:
        collections = [line.strip() for line in x]
        collections = [s.replace('Â','') for s in collections]

    return collections


def getKanHTML(kanID):
    kURL = kanURL
    kID = kanID

    # kURLFull = kanURL+kanID
    print(kanID)

    r = requests.get(kanID)
    kHTML = r.text

    #test that we have access to video
    badText = 'Your search has not matched any results'

    if badText in kHTML:
        soup = '-1'
        # print('bad text found')
        return soup
    else:
        soup = BeautifulSoup(kHTML)
        return soup

def parseHTML(soup):

    collList = []
    for a in soup.find_all('div'):
        if a.has_attr('class') and a['class'][0] == 'breadcrumb':
            collList.append(a.text)

    collList = [s.replace(' show more', '') for s in collList]
    collList = [s.replace(' \xa0', '') for s in collList]

    return collList

def testKanopy(kanopyID,titCollection):
    pdaCollections = loadCollections()

    # collection = titCollection[titCollection.rfind('from')+5:len(titCollection)]
    # title = titCollection[:titCollection.find('from')].strip()

    PDAgroup = None

    unknownCollection = []
    for collection in titCollection:

        if collection in pdaCollections:
            PDAgroup = True
            return PDAgroup
        elif collection == 'Media Education Foundation':
            PDAgroup = False
            return PDAgroup
        else:
            unknownCollection.append(kanopyID)

    for kanopyID in unknownCollection:
        webbrowser.open(kanopyID, new=1)
        PDAgroupResponse = input('Is '+kanopyID+' a PDA Title? \nTrue or False')
        if PDAgroupResponse in(True, 'true', 't', 'T', 'True'):
            PDAgroup = True
        else:
            PDAgroup = False

    return PDAgroup

def runKanopy(kanID):
    soup = getKanHTML(kanID)
    # print ('soup is: ', soup)
    if soup == '-1':
        print("video not accessible")

        PDAGroup = None
        return PDAGroup

    titCollection = parseHTML(soup)

    print(titCollection)
    # collection = titCollection[titCollection.rfind('from')+5:len(titCollection)]
    # title = titCollection[:titCollection.find('from')].strip()

    PDAGroup = testKanopy(kanID,titCollection)

    return PDAGroup
    print (soup)

def writeToPDAFile(record, file):
    with open(file, 'ab') as x:
        try:
            x.write((record.as_marc()))
        except UnicodeEncodeError:
            print ("couldn't write")
    print("Written!")


def openKanopyMarc():
    marcFile = 'C:\\Users\\fenichele\\Desktop\\Kanopy_MARC_Records__fau.kanopystreaming.com__1-Jun-2015.mrc'

    from tkinter import  filedialog
    marcPath = tkinter.filedialog.askopenfile()
    marcFile = marcPath.name

    with open(marcFile, 'rb') as fh:
        reader = MARCReader(fh)

        kanURLs = []
        for record in reader:
            kU= record.get_fields('856')
            for url in kU:
                kanURLs.append(url['u'])

        for kanLink in kanURLs:
            isPDA = runKanopy(kanLink)

            # lockanID = record['001'].value()
            # lockanID = lockanID.strip('kan')

            print(kanLink, 'is pda:', isPDA)

            if isPDA is True:
                writeToPDAFile(record,pdaKanopyMarcFile)
            elif isPDA is False:
                writeToPDAFile(record,licenseKanopyMarcFile)
            elif isPDA is None:
                "PDA is not applicable b/c we don't have access"
            else:
                "PDA is Unknown!"

                print('\n')


openKanopyMarc()