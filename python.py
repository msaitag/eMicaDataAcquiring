import pandas as pd
import multiprocessing
from multiprocessing.dummy import Pool
from random import random
from eMicaContentAnalysis.eMicaItemDedector import *
import json
import csv
import time

with open('eMicaContentAnalysis/jsonFiles/hotelinlinks.json', 'r') as link:
    hotelinlinks = json.load(link)


def itemCheck(websites, retDict, item):
    i = websites
    itemCheck = item(hotelinlinks[i])
    if len(itemCheck) > 0:
        check = 2
    else:
        check = 1
    score = {hotelinlinks[i]['id']: check}
    retDict[websites] = score


def multipro(item, lenght):
    man = multiprocessing.Manager()
    retDict = man.dict()
    p = Pool(processes=4)

    for i in range(lenght):
        p.apply_async(func=itemCheck, args=(i, retDict, item))
    p.close()
    p.join()
    datas = retDict.values()
    return datas


def writeResults(arr, item):
    import pandas as pd

    results = arr
    itemC = item
    df = pd.read_csv('eMicaContentAnalysis/csvFiles/results.csv')

    df[itemC] = results
    print(df)
    df.to_csv('eMicaContentAnalysis/csvFiles/results.csv', index=False)


def start():
    if __name__ == '__main__':
        start = time.time()
        x = len(hotelinlinks)

        item = hotelPrivacy
        itemCol = 'hotelPrivacy'
        lenght = x
        scores = multipro(item, lenght)

        array = []
        padding = 3
        dict = scores[0]
        for i in range(1, len(scores)):
            dict = dict | scores[i]
        for i in range(1, len(dict)+1):
            x = str(i).zfill(padding)
            array.append(dict[x])

        if lenght == len(hotelinlinks):
            writeResults(array, itemCol)
        print(array)
        print(scores)
        end = time.time()
        print((end-start)/60)


def csvToExcel():
    df = pd.read_csv('eMicaContentAnalysis/csvFiles/results.csv')
    df.to_excel('eMicaContentAnalysis/excelFiles/results.xlsx',
                index=False, header=True)


def csvWriter():
    import pandas as pd

    with open('eMicaContentAnalysis/jsonFiles/hotelinlinks.json', 'r') as file:
        hotelInlinks = json.load(file)

    urls = []
    for i in range(len(hotelInlinks)):
        url = hotelInlinks[i]['domain']
        urls.append(url)

    rawData = {
        'websites': urls
    }
    df = pd.DataFrame(rawData, columns=['websites'])
    df.to_csv('eMicaContentAnalysis/csvFiles/results.csv', index=False)


def checkData(x, y):
    import pandas as pd

    df = pd.DataFrame(x | y, columns=['websites', 'scores'])
    df.to_csv(
        'eMicaContentAnalysis/csvFiles/check.csv', index=False)


def csvToExcel2():
    df = pd.read_csv('eMicaContentAnalysis/csvFiles/check.csv')
    df.to_excel('eMicaContentAnalysis/excelFiles/check.xlsx',
                index=False, header=True)


def websiteCheck():
    import random
    with open('eMicaContentAnalysis/jsonFiles/hotelinlinks.json', 'r') as link:
        hotelInlinks = json.load(link)
    with open('eMicaContentAnalysis/csvFiles/results.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        data = {d['websites']: d['hotelRoom'] for d in list(reader)}
    checkWebsite = []
    checkScore = []
    ranNum = []
    array = []
    padding = 3
    x = random.sample(range(1, 261), 26)
    print(x)
    for i in x:
        y = str(i).zfill(padding)
        ranNum.append(y)
    for j in ranNum:

        for i in range(len(hotelInlinks)):
            if hotelInlinks[i]['id'] == j:
                website = hotelInlinks[i]['domain']
                score = data.get(website, 'Not Found')
                scores = {website: score}
                array.append(scores)

                checkWebsite.append(website)
                checkScore.append(score)
                x = {
                    'websites': checkWebsite
                }
                y = {
                    'scores': checkScore
                }
                checkData(x, y)
                csvToExcel2()
    return array


# csvToExcel()

# print(websiteCheck())

start()
