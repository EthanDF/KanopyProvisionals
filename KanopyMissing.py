from pymarc import *

missingList = []
missingFile = 'c:\\users\\fenichele\\Desktop\\kanopyMissing.txt'

marcFile = 'c:\\users\\fenichele\\Desktop\\kanopyPDA.mrc'

outputMarcFile = 'c:\\users\\fenichele\\Desktop\\kanopyPDAmissing.mrc'

def loadMissingList():

    with open(missingFile) as f:
        content = f.readlines()

    for c in content:
        missingList.append(c.strip('\n'))

    return missingList

def writeMarc(record):
    with open(outputMarcFile, 'ab') as x:
        try:
            x.write((record.as_marc()))
        except UnicodeEncodeError:
            print("couldn't write")
            input('press any key to continue')
    # print("Written!")


def checkMarc():

    # get list of IDs
    missingList = loadMissingList()

    #load Marc
    with open(marcFile, 'rb') as fh:
        reader = MARCReader(fh, to_unicode=True, force_utf8=True)

        for record in reader:
            recID = record['001'].value()

            if recID in missingList:
                print(recID, ": True")
                writeMarc(record)
            else:
                print(recID, ": False")
            #
            # keepGoing = input("continue?")
            # if keepGoing == 'n':
            #     return  record



