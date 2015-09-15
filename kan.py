from bs4 import BeautifulSoup
from pymarc import *
import urllib.request
# import requests
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
    collectionList = 'C:\\Users\\fenichele\\github\\KanopyCollection\\kanopy_pda_producers.txt'

    collections = []
    with open(collectionList, 'r') as x:
        collections = [line.strip() for line in x]

    return collections


def getKanHTML(kanID):
    kURL = kanURL
    kID = kanID

    kURLFull = kanID
    print(kURLFull)

    # r = requests.get(kURLFull)
    with urllib.request.urlopen(kURLFull) as r:
        kHTML = r.read().decode()

    #test that we have access to video
    badText = 'Your search has not matched any results'

    if badText in str(kHTML):
        soup = '-1'
        # print('bad text found')
        return soup
    else:
        soup = BeautifulSoup(kHTML)
        return soup

def parseHTML(soup):

    coll = None
    # for a in soup.find_all('div'):
    #     if a.has_key('class') and a['class'][0] == 'title':
    #         coll = a.text
    #search soup for h1 values
    h = soup.find_all('h1')
    # print(h)
    # h1 = h[0].find_all('span')
    # print(h1)
    coll = h[0].find_all('a')[-1].string

    return coll

def checkCategories(soup):

    cats = []
    my_divs = soup.findAll('div', {"class" : "breadcrumb"})

    if len(my_divs) == 0:
        return cats
    else:
        for div in my_divs:
            m = 0
            while m < len(div):
                cats.append(div.contents[m].string)
                m += 1

    return cats

def loadCategories():
    categoryList = 'C:\\Users\\fenichele\\github\\KanopyCollection\\kanopy_pda_categories.txt'

    categories = []
    with open(categoryList, 'r') as x:
        categories = [line.strip() for line in x]

    return categories

def testCategories(pdaCategories, titleCategories):

    found = False
    for cat in titleCategories:
        if cat in pdaCategories:
            found = True

    return found

def testKanopy(kanopyID,titCollection, categories):
    pdaCollections = loadCollections()

    pdaCategories = loadCategories()

    collection = titCollection
    # title = titCollection[:titCollection.find('from')].strip()

    PDAgroup = None

    if collection in pdaCollections:
        PDAgroup = True
    elif testCategories(pdaCategories, categories):
        PDAgroup = True
    elif collection == 'Media Education Foundation':
        PDAgroup = False
    else:
        webbrowser.open(kanopyID, new=1)
        PDAgroupResponse = input('Is '+titCollection+' a PDA Title? \nTrue or False')
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
    categoryList = checkCategories(soup)

    print(titCollection)
    print(categoryList)
    # collection = titCollection[titCollection.rfind('from')+5:len(titCollection)]
    # title = titCollection[:titCollection.find('from')].strip()

    PDAGroup = testKanopy(kanID, titCollection, categoryList)

    return PDAGroup
    # print (soup)

def writeToPDAFile(record, file):
    with open(file, 'ab') as x:
        try:
            x.write((record.as_marc()))
        except UnicodeEncodeError:
            print ("couldn't write")
    print("Written!")


def openKanopyMarc():
    marcFile = 'C:\\Users\\fenichele\\Desktop\\Kanopy_MARC_Records__www.kanopystreaming.com__14-Sep-2015\\Kanopy_MARC_Records__www.kanopystreaming.com__14-Sep-2015.mrc'

    # from tkinter import  filedialog
    # marcPath = tkinter.filedialog.askopenfile()
    # marcFile = marcPath.name

    with open(marcFile, 'rb') as fh:
        reader = MARCReader(fh)

        for record in reader:
            lockanID = record['856']['u']
            lockanID = lockanID.strip('kan')

            isPDA = runKanopy(lockanID)
            print(lockanID, 'is pda:', isPDA)

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