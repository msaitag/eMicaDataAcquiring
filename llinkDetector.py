

hotelname = 'samir'
citycode = '34'
domain = 'http://www.samirhotel.com/tr/'
rawdomain = 'http://www.samirhotel.com/tr/'


def linkDetector(hotel, city, dom, rawdom):
    from unidecode import unidecode
    import requests
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import json
    from time import sleep

    hotelname = hotel
    citycode = city
    domain = dom
    rawdomain = rawdom
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get(domain)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    browser.close()

    links = []
    inlinks = []
    exinlinks = []
    brokelinks = []
    pic = ['.jpg', '.png', 'java',
           'tel:', '@', '.pdf', 'telefon', 'telephone', 'callto', 'mailto']

    for link in soup.find_all('a'):
        href = link.get('href')
        links.append(href)
        if href != None and href != '':
            lastChar = href[-1]
            if 'http' not in str(href):
                if str(href[0]) != '#':
                    if str(href[0]) == '/':
                        href = href[1:] + ''
                    if str(lastChar) == '/':
                        href = href[:-1] + ''
                    url = str(rawdomain) + str(href.replace(' ', ''))
                    urlRaw = unidecode(url.lower())
                    if url not in inlinks:
                        if not any(x in urlRaw for x in pic):
                            inlinks.append(url)
            elif 'http' in str(href):
                if str(href[0]) != '#':
                    if rawdomain in str(href):
                        if str(href[-2:]) == '//':
                            href = href[:-1] + ''
                        if str(href) not in inlinks:
                            if not any(x in str(href) for x in pic):
                                inlinks.append(str(href))

    user_agent = {
        'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.104 Safari/537.36 Edge/107.0.1418.24'}

    for link in inlinks:
        try:
            statusCode = requests.get(
                link, headers=user_agent, verify=False, timeout=20).status_code

            if statusCode == 200:
                exinlinks.append(link)
            else:
                brokelinks.append(link)

        except:
            brokelinks.append(link)
            # statusCode = requests.get(
            #     link, headers=user_agent, verify=False, timeout=20).status_code
            # if statusCode == 200:
            #     exinlinks.append(link)
            # else:
            #     brokelinks.append(link)

    print('All Links on the Page \n', links)
    print('All inLinks on the Page \n', inlinks)
    print('Exract of inLinks from the Page \n', exinlinks)
    print('All Broken Links on the Page \n', brokelinks)

    with open('eMicaContentAnalysis/jsonFiles/hotelinlinks.json', 'r') as file:
        data = json.load(file)
    i = len(data) + 1
    padding = 3
    id = str(i).zfill(padding)

    Inlinks = {
        'id': id,
        'domain': domain,
        'hotelname': hotelname,
        'citycode': citycode,
        'rawdomain': rawdomain,
        'inlinks': exinlinks
    }
    # hotelInlinks = [Inlinks]

    # with open('eMicaContentAnalysis/jsonFiles/hotelinlinks.json', 'r+', encoding='utf-8') as file:
    #     data = json.load(file)
    #     data.append(Inlinks)
    #     file.seek(0)
    #     json.dump(data, file, ensure_ascii=False)
    data.append(Inlinks)
    with open('eMicaContentAnalysis/jsonFiles/hotelinlinks.json', 'w', encoding='utf-8') as file:
        json.dump(data, file)


linkDetector(hotelname, citycode, domain, rawdomain)
