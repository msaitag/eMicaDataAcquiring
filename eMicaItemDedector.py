from dataclasses import replace
from datetime import datetime
from distutils.log import error
from multiprocessing.resource_sharer import stop
from time import sleep, strftime, time
from unidecode import unidecode
import json

# with open('hotelinlinks.json', 'r') as link:
#     data = json.load(link)

with open('eMicaContentAnalysis/jsonFiles/cities.json', 'r') as link2:
    cities = json.load(link2)


def webdriver(domain):
    from selenium import webdriver
    from bs4 import BeautifulSoup

    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get(domain)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    browser.close()
    return soup


def statuscode(link):
    import requests

    user_agent = {
        'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.104 Safari/537.36 Edge/107.0.1418.35'}
    try:
        statusCode = requests.get(
            link, headers=user_agent, timeout=10).status_code
    except:
        statusCode = requests.get(
            link, headers=user_agent, verify=False, timeout=10).status_code

    return statusCode


def xpathclick(domain, xpath):
    from selenium import webdriver
    from selenium.webdriver.support.select import By
    import time
    url = ''
    try:
        driver = webdriver.Chrome()
        driver.get(domain)
        l = driver.find_element(by=By.XPATH, value=xpath)
        driver.execute_script("arguments[0].click();", l)
        time.sleep(5)
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[1])
        url = driver.current_url
        driver.quit()
    except:
        pass
    return url


def hotelPhone(website):
    print(website['domain'])
    print(website['id'])
    hotelphone = []
    cityCode = website['citycode']
    phoneCode = cities[cityCode]['phoneCode']
    contactObjects = ['ulasin', 'contact', 'iletisim']
    array = []
    try:
        soup = webdriver(website['domain'])
        array.append(website['domain'])
        for tag in soup.find_all('a'):
            tagText = tag.get_text()
            tagText = unidecode(str(tagText).lower())
            if any(x in tagText for x in contactObjects):
                href = str(tag.get('href'))
                if len(href) > 0 and href[-1] == '/':
                    href = href[:-1]
                for url in website['inlinks']:
                    if href in url:
                        array.append(url)
        for link in array:
            soup = webdriver(link)
            for tag in soup.find_all(['span', 'p', 'li', 'td', 'a', 'div']):
                content = str(tag.get_text())
                phone = ''
                for i in content:
                    if i.isdigit():
                        phone += i
                if len(content) > 0 and len(phone) > 9 and any(x in phone for x in phoneCode) and len(content) < 300:
                    if phone not in hotelphone:
                        hotelphone.append(phone)
            if len(hotelphone) > 0:
                break
            else:
                continue
    except:
        pass
    return hotelphone


def hotelPhoneHyper(website):
    print(website['id'])
    print(website['domain'])
    hotel_phone_hyper = []
    cityCode = website['citycode']
    phoneCode = cities[cityCode]['phoneCode']
    contactObjects = ['ulasin', 'contact', 'iletisim']
    array = []
    array.append(website['domain'])
    soup = webdriver(website['domain'])
    for tag in soup.find_all('a'):
        tagText = tag.get_text()
        tagText = unidecode(str(tagText).lower())
        if any(x in tagText for x in contactObjects):
            href = str(tag.get('href'))
            if len(href) > 0 and href[-1] == '/':
                href = href[:-1]
            for url in website['inlinks']:
                if href in url:
                    array.append(url)
    for link in array:
        soup = webdriver(link)
        for tag in soup.find_all(['a']):
            try:
                content = str(tag.get_text())
                phone = ''
                for i in content:
                    if i.isdigit():
                        phone += i
                if len(phone) > 9 and any(x in phone for x in phoneCode):
                    if phone not in hotel_phone_hyper:
                        hotel_phone_hyper.append(phone)
            except:
                pass
        if len(hotel_phone_hyper) > 0:
            break
        else:
            continue

    return hotel_phone_hyper


def hotelMail(website):
    print(website['id'])
    print(website['domain'])
    contactObjects = ['contact', 'iletisim', 'ulasin']
    hotelMail = []
    searchObjects = ['reservation', 'info',
                     website['hotelname'], 'rezervasyon']
    emailObjects = ['@', '.com']
    array = []
    try:
        array.append(website['domain'])
        soup = webdriver(website['domain'])

        for tag in soup.find_all('a'):
            tagText = tag.get_text()
            tagText = unidecode(str(tagText).lower())
            if any(x in tagText for x in contactObjects):
                href = str(tag.get('href'))
                if len(href) > 0 and href[-1] == '/':
                    href = href[:-1]
                for url in website['inlinks']:
                    if href in url:
                        array.append(url)
        for link in array:
            soup = webdriver(link)
            for tag in soup.find_all(['li', 'span', 'p', 'td', 'a', 'div']):
                content = tag.get_text()
                if len(content) > 0 and len(content) < 300:
                    content = unidecode(str(content).lower())
                    if all(x in content for x in emailObjects) and any(x in content for x in searchObjects):
                        hotelMail.append(content.replace(' ', ''))
            if len(hotelMail) > 0:
                break
            else:
                continue
    except:
        pass
    return hotelMail


def hotelFax(website):
    print(website['domain'])
    print(website['id'])
    fax = ['fax', 'faks', 'f:']
    contactObjects = ['ulasin', 'contact', 'iletisim']
    hotelfax = []
    cityCode = website['citycode']
    phoneCode = cities[cityCode]['phoneCode']
    array = []
    array.append(website['domain'])
    soup = webdriver(website['domain'])
    for tag in soup.find_all('a'):
        tagText = tag.get_text()
        tagText = unidecode(str(tagText).lower())
        if any(x in tagText for x in contactObjects):
            href = str(tag.get('href'))
            if len(href) > 0 and href[-1] == '/':
                href = href[:-1]
            for url in website['inlinks']:
                if href in url:
                    array.append(url)
    for link in array:
        soup = webdriver(link)
        for tag in soup.find_all(['a', 'span', 'p', 'li', 'td', 'div']):
            content = str(tag.get_text())
            content = unidecode(content.lower())
            phone = ''
            for i in content:
                if i.isdigit():
                    phone += i
            if len(phone) > 9 and any(x in phone for x in phoneCode):

                if any(x in content for x in fax) and len(content) < 300:
                    hotelfax.append(content)
                else:
                    for link in tag.find_all(['img', 'i']):
                        src = link.get('src')
                        clas = link.get('class')
                        if 'fax' in str(src).lower():
                            hotelfax.append(str(src) + ' ' + phone)
                        elif 'fax' in str(clas).lower():
                            hotelfax.append(str(clas) + ' ' + phone)
        if len(hotelfax) > 0:
            break
        else:
            continue
    return hotelfax


def hotelOnRezerv(website):
    print(website['domain'])
    print(website['id'])
    hotelRezerv = []
    hotelRezervCheckIn = []
    hotelRezervCheckOut = []
    rezItem = ['rezervasyon', 'reservation', 'booking', 'book']
    checkInItems = ['checkin', 'arrival', 'startdate']
    checkOutItems = ['checkout', 'departure', 'enddate']
    link = ['src', 'url']
    soup = webdriver(website['domain'])
    try:
        for tag in soup.find_all('div'):
            for input in tag.find_all('input'):
                input = unidecode(str(input).lower())
                inputRaw = ''
                for i in input:
                    if i.isalpha():
                        inputRaw += i
                if any(x in inputRaw for x in checkInItems):
                    hotelRezervCheckIn = []
                    hotelRezervCheckIn.append(input)
                if any(x in inputRaw for x in checkOutItems):
                    hotelRezervCheckOut = []
                    hotelRezervCheckOut.append(input)
        hotelRezerv = hotelRezervCheckIn + hotelRezervCheckOut
        if len(hotelRezerv) < 1:
            for script in soup.find_all('script'):
                script = unidecode(str(script).lower())
                if any(x in script for x in rezItem) and any(x in script for x in link) and 'http' in script:
                    hotelRezerv = []
                    hotelRezerv.append(script)
        if len(hotelRezerv) < 1:
            soup = webdriver(website['domain'])
            for link in soup.find_all('a'):
                link = unidecode(str(link).lower())
                if any(x in link for x in rezItem):
                    if str(website['domain']) not in link:
                        hotelRezerv = []
                        hotelRezerv.append(link)
        if len(hotelRezerv) < 1:
            array = []
            soup = webdriver(website['domain'])
            for tag in soup.find_all('a'):
                tagT = tag.get_text()
                href = tag.get('href')
                if len(tagT) > 0:
                    tagR = unidecode(str(tagT).lower())
                    if any(x in tagR for x in rezItem) and href > 0 and '@' not in href:
                        if href not in array:
                            array.append(href)
            for url in array:
                soup = webdriver(url)
                for tag in soup.find_all('div'):
                    for input in tag.find_all('input'):
                        input = unidecode(str(input).lower())
                        inputRaw = ''
                        for i in input:
                            if i.isalpha():
                                inputRaw += i
                        if any(x in inputRaw for x in checkInItems):
                            hotelRezervCheckIn = []
                            hotelRezervCheckIn.append(input)
                        if any(x in inputRaw for x in checkOutItems):
                            hotelRezervCheckOut = []
                            hotelRezervCheckOut.append(input)
                hotelRezerv = hotelRezervCheckIn + hotelRezervCheckOut

    except:
        pass

    return hotelRezerv


def hotelAddress(website):
    print(website['id'])
    print(website['domain'])
    hotelAdress = []
    cCode = website['citycode']
    cDistricts = cities[cCode]['districts']
    cName = cities[cCode]['cityName']
    if cName in cDistricts:
        cityInfo = [[cCode], cDistricts, ['turkey', 'turkiye', 'turkei']]
    else:
        cityInfo = [[cCode], cDistricts, [cName], ['turkey', 'turkiye']]

    contactObjects = ['ulasin', 'contact', 'iletisim']
    array = []
    array.append(website['domain'])
    soup = webdriver(website['domain'])
    for tag in soup.find_all('a'):
        tagText = tag.get_text()
        tagText = unidecode(str(tagText).lower())
        if any(x in tagText for x in contactObjects):
            href = str(tag.get('href'))
            if len(href) > 0 and href[-1] == '/':
                href = href[:-1]
            for url in website['inlinks']:
                if href in url:
                    array.append(url)
    for link in array:
        soup = webdriver(link)
        for tag in soup.find_all(['li', 'td', 'p', 'span', 'div']):
            content = tag.get_text()
            content = unidecode(str(content).lower())
            count = 0
            for item in cityInfo:
                if any(x in content for x in item):
                    count += 1
            if count > 1 and len(content) < 300:
                hotelAdress.append(tag)
        if len(hotelAdress) > 0:
            break
        else:
            continue
    return hotelAdress


def hotelPrivacy(website):
    print(website['id'])
    print(website['domain'])
    hotelPrivacy = []
    privacyItems = ['privacy', 'gizlilik', 'kvkk',
                    'gdpr', 'kisiselveri', 'personaldata']
    try:
        soup = webdriver(website['domain'])
        for tag in soup.find_all(['a', 'button']):
            tagText = unidecode(str(tag).lower())
            tagRaw = ''
            for i in tagText:
                if i.isalpha():
                    tagRaw += i
            if any(x in tagRaw for x in privacyItems):
                hotelPrivacy.append(tag)
    except:
        pass
    return hotelPrivacy


def hotelCookie(website):
    print(website['id'])
    print(website['domain'])
    hotelPrivacy = []
    privacyItems = ['cookie', 'cerez']

    soup = webdriver(website['domain'])
    for tag in soup.find_all(['a', 'button']):
        try:
            tagRaw = unidecode(str(tag).lower())
            if any(x in tagRaw for x in privacyItems):
                hotelPrivacy.append(tag)
        except:
            pass

    return hotelPrivacy


def hotelAbout(website):
    print(website['id'])
    print(website['domain'])
    soup = webdriver(website['domain'])
    hotel_about = []
    searchItems = ['about', 'hakkimizda',
                   'kimiz', 'company', 'hikayemiz', 'story', 'kurumsal', 'hakkinda']
    for tag in soup.find_all(['a']):
        tagT = tag.get_text()
        if len(tagT) > 0:
            tagT = unidecode(str(tagT).lower())
            if any(x in tagT for x in searchItems):
                hotel_about.append(tag.get('href'))

    return hotel_about


def hotelMailHyper(website):
    print(website['domain'])
    print(website['id'])
    hotelMail = []
    emailObjects2 = ['reservation', 'info',
                     website['hotelname'], 'rezervasyon']
    emailObjects = ['@', '.com']
    contactObjects = ['ulasin', 'contact', 'iletisim']
    array = []
    soup = webdriver(website['domain'])
    array.append(website['domain'])
    for tag in soup.find_all('a'):
        tagText = tag.get_text()
        tagText = unidecode(str(tagText).lower())
        if any(x in tagText for x in contactObjects):
            href = str(tag.get('href'))
            if len(href) > 0 and href[-1] == '/':
                href = href[:-1]
            for url in website['inlinks']:
                if href in url:
                    array.append(url)
    for link in array:
        soup = webdriver(link)
        for link2 in soup.find_all(['a']):
            try:
                content = unidecode(str(link2).lower())
                if all(x in content for x in emailObjects) and any(x in content for x in emailObjects2):
                    hotelMail.append(content.replace(' ', ''))

            except:
                pass
        if len(hotelMail) > 0:
            break
        else:
            continue
    return hotelMail


def hotelRoom(website):
    print(website['id'])
    print(website['domain'])
    hotelrooms = []
    hotel_room = ['rooms', 'odalar', 'accommodation', 'konaklama', 'stay']
    soup = webdriver(website['domain'])
    for tag in soup.find_all(['a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        try:
            tagT = tag.get_text()
            tagT = unidecode(str(tag).lower())
            if any(x in tagT for x in hotel_room):
                hotelrooms.append(tag)
        except:
            pass

    return hotelrooms


def hotelRestaurant(website):
    print(website['id'])
    print(website['domain'])
    hotelrestaurants = []
    hotelRestItems = ['restaurant', 'restoran',
                      'yeme', 'gastronomi', 'food', 'yiyecek', 'dining']
    soup = webdriver(website['domain'])
    for tag in soup.find_all(['a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        try:
            tagT = tag.get_text()
            tagT = unidecode(str(tagT).lower())
            if any(x in tagT for x in hotelRestItems) and tag not in hotelrestaurants:
                hotelrestaurants.append(tag)
        except:
            pass
    return hotelrestaurants


def hotelMeeting(website):
    print(website['id'])
    print(website['domain'])
    hotelmeeting = []
    searchItems = ['meeting', 'toplanti', 'konferans', 'conference']
    soup = webdriver(website['domain'])
    for tag in soup.find_all(['a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        try:
            tagT = tag.get_text()
            tagT = unidecode(str(tagT).lower())
            if any(x in tagT for x in searchItems):
                hotelmeeting.append(tagT)
        except:
            pass
    return hotelmeeting


def hotelGallery(website):
    print(website['id'])
    print(website['domain'])
    hotelgallery = []
    searchItems = ['gallery', 'galeri', 'photo',
                   'resim', 'album', 'fotograf', 'picture']
    soup = webdriver(website['domain'])
    for tag in soup.find_all(['a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        try:
            tagT = tag.get_text()
            tagT = unidecode(str(tagT).lower())
            if any(x in tagT for x in searchItems):
                hotelgallery.append(tagT)
        except:
            pass
    return hotelgallery


def hotelMap(website):
    print(website['id'])
    print(website['domain'])
    hotel_map = []
    searchItems = [['google', 'map', 'http'], [
        'map', 'yandex', 'http'], ['map', 'baidu', 'http']]
    contactObjects = ['ulasin', 'contact', 'iletisim', 'konum', 'location']
    statusCode = [200, 302, 303]
    array = []
    soup = webdriver(website['domain'])
    for tag in soup.find_all('a'):
        tagText = tag.get_text()
        tagText = unidecode(str(tagText).lower())
        if any(x in tagText for x in contactObjects):
            href = tag.get('href')
            if href != None:
                if len(href) > 0 and not href[-1].isalnum():
                    href = href[:-1]
                for url in website['inlinks']:
                    if href in url:
                        array.append(url)
    array.append(website['domain'])
    for link in array:
        soup = webdriver(link)
        for tag in soup.find_all(['iframe', 'link', 'a', 'script', 'img']):
            try:
                tagS = tag.get('src')
                tagH = tag.get('href')
                if tagS != None:
                    url = tagS
                else:
                    url = tagH
                for i in searchItems:
                    if all(x in str(url).lower() for x in i):
                        try:
                            for j in statusCode:
                                if statuscode(url) == j:
                                    hotel_map.append(url)
                        except:
                            pass
            except:
                pass
        if len(hotel_map) > 0:
            break
        else:
            continue
    return hotel_map


def hotelWeather(website):
    print(website['id'])
    print(website['domain'])
    searchItems = ['weather', 'temperature']
    hotelweather = []
    contactObjects = ['ulasin', 'contact', 'iletisim']
    array = []
    soup = webdriver(website['domain'])
    for tag in soup.find_all('a'):
        tagText = tag.get_text()
        tagText = unidecode(str(tagText).lower())
        if any(x in tagText for x in contactObjects):
            href = str(tag.get('href'))
            if href != None:
                if len(href) > 0 and not href[-1].isalnum():
                    href = href[:-1]
                for url in website['inlinks']:
                    if href in url:
                        array.append(url)
    array.append(website['domain'])
    for link in array:
        soup = webdriver(link)
        for tag in soup.find_all('div'):
            try:
                tagT = tag.get_text()
                if any(x in str(tag).lower() for x in searchItems):
                    hotelweather.append(tagT)
            except:
                pass
    return hotelweather


def hotelTime(website):
    time = int(strftime('%H:%M').replace(':', ''))
    timeArray = []
    timeArray.append(str(time))
    newTime = time
    j = 1
    for i in range(2):
        newTime += j
        time -= j
        timeArray.append(str(newTime))
        timeArray.append(str(time))

    if time > 1259:
        for t in range(len(timeArray)):
            pm = int(timeArray[t])
            pm -= 1200
            timeArray.append(str(pm))

    print(website['id'])
    print(website['domain'])
    hotel_time = []
    # contactObjects = ['ulasin', 'contact', 'iletisim']
    # array = []
    # array.append(website['domain'])
    # for tag in soup.find_all('a'):
    #     tagText = tag.get_text()
    #     tagText = unidecode(str(tagText).lower())
    #     if any(x in tagText for x in contactObjects):
    #         href = str(tag.get('href'))
    #         if len(href) > 0 and href[-1] == '/':
    #             href = href[:-1]
    #         for url in website['inlinks']:
    #             if href in url:
    #                 array.append(url)
    # searchItems = ['localtime', 'yerelsaat']
    soup = webdriver(website['domain'])
    try:
        for tag in soup.find_all(['span', 'li', 'p', 'h1', 'h2', 'h3', 'h4', 'h5']):
            tagText = tag.get_text()
            divRaw = ''
            for i in tagText:
                if i.isdigit():
                    divRaw += i
            if any(x in divRaw for x in timeArray) and len(divRaw) < 7:
                hotel_time = []
                hotel_time.append(tag.get_text())
    except:
        pass
    return hotel_time


def hotelSitemap(website):
    print(website['id'])
    print(website['domain'])
    hotel_sitemap = []
    searchItems = ['sitemap', 'siteharita']
    soup = webdriver(website['domain'])
    for tag in soup.find_all('a'):
        try:
            tagT = tag.get_text()
            if len(tagT) > 0:
                tagRaw = unidecode(str(tagT).lower())
                aRaw = ''
                for i in tagRaw:
                    if i.isalpha():
                        aRaw += i
                if any(x in aRaw for x in searchItems):
                    hotel_sitemap.append(tag)
        except:
            pass
    return hotel_sitemap


def hotelUser(website):
    print(website['id'])
    print(website['domain'])
    hotel_user = []
    searchItems = ['login', 'logout', 'signin', 'signout', 'signup']
    soup = webdriver(website['domain'])
    for tag in soup.find_all(['a', 'button']):
        try:
            tagText = unidecode(str(tag).lower())
            tagRaw = ''
            for i in tagText:
                if i.isalpha():
                    tagRaw += i
            if any(x in tagRaw for x in searchItems):
                hotel_user.append(tag)
        except:
            pass
    return hotel_user


def hotelFaq(website):
    print(website['id'])
    print(website['domain'])
    hotel_faq = []
    searchItems = ['sikcasorulan', 'frequentlyask']
    searchItems2 = ['faq', 'sss']
    soup = webdriver(website['domain'])
    for tag in soup.find_all('a'):
        try:
            tagText = tag.get_text()
            if len(tagText) > 0:
                tagRaw = unidecode(str(tagText).lower())
                textRaw = ''
                for i in tagRaw:
                    if i.isalpha():
                        textRaw += i
                if any(x in textRaw for x in searchItems) or any(x in tagRaw for x in searchItems2):
                    hotel_faq.append(tag)
        except:
            pass
    return hotel_faq


def hotelOffers(website):
    print(website['id'])
    print(website['domain'])
    searchItems = ['offer', 'teklif']
    hotel_offers = []
    soup = webdriver(website['domain'])
    for tag in soup.find_all('a'):
        try:
            tagText = tag.get_text()
            if len(tagText) > 0:
                tagRaw = unidecode(str(tagText).lower())
                if any(x in tagRaw for x in searchItems):
                    hotel_offers.append(tag)
        except:
            pass
    return hotel_offers


def hotelVideo(website):
    print(website['id'])
    print(website['domain'])
    searchItems = ['video']
    searchItems2 = [['youtube', 'watch'], ['.mp4'], ['youtube', 'embed']]
    hotel_video = []
    soup = webdriver(website['domain'])
    for tag in soup.find_all(['video', 'iframe', 'a']):
        try:
            if tag.get('href') != None:
                href = tag.get('href')
                for i in searchItems2:
                    if all(x in href for x in i):
                        hotel_video.append(tag)
            elif tag.get('src') != None:
                src = tag.get('src')
                for i in searchItems2:
                    if all(x in src for x in i):
                        hotel_video.append(tag)
            if len(hotel_video) > 0:
                break
            else:
                tagText = unidecode(str(tag).lower())
                if any(x in tagText for x in searchItems):
                    hotel_video.append(tag)
        except:
            pass
    return hotel_video


def hotelVirtual(website):
    print(website['id'])
    print(website['domain'])
    searchItems = [['virtual', 'tour'], [
        'sanal', 'gezinti'], ['sanal', 'tur'], ['360']]
    hotel_virtual = []
    soup = webdriver(website['domain'])
    for tag in soup.find_all(['a']):
        try:
            href = tag.get('href')
            tagText = tag.get_text()
            if len(tagText) > 0:
                tagText = unidecode(str(tagText).lower())
                for i in searchItems:
                    if all(x in tagText for x in i):
                        hotel_virtual.append(href)
        except:
            pass
    return hotel_virtual


def hotelLang(website):
    from googletrans import Translator
    inlinks = website['inlinks']
    domain = website['domain']
    hotel_lang = []
    langs = []
    searchItems = []
    exludeItems = ['instagram', 'facebook', 'twitter', 'youtube']
    try:
        for link in inlinks:
            soup = webdriver(link)
            try:
                for tag in soup.find_all('html'):
                    tLang = tag.get('lang')
                if tLang != None and tLang not in langs:
                    langs.append(tLang)
            except:
                pass
    except:
        pass
    if len(langs) > 1:
        hotel_lang.append(langs)
    return hotel_lang


def hotelNewsletter(website):
    print(website['id'])
    print(website['domain'])
    searchItems = ['newsletter', 'ebulten', 'bulten']
    hotel_newsletter = []
    soup = webdriver(website['domain'])
    for tag in soup.find_all('div'):
        try:
            tagRaw = unidecode(str(tag).lower())
            tagText = ''
            for let in tagRaw:
                if let.isalpha():
                    tagText += let
            if any(x in tagText for x in searchItems):
                hotel_newsletter.append(tag)
        except:
            pass

    return hotel_newsletter


def hotelAwards(website):
    # also could be use the h tags for searching
    print(website['id'])
    print(website['domain'])
    searchItems = ['awards', 'oduller']
    hotel_awards = []
    try:
        soup = webdriver(website['domain'])
        for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'div']):
            tagH = tag.get_text()
            if len(tagH) > 0:
                tagH = unidecode(str(tagH).lower())
                if any(x in tagH for x in searchItems):
                    hotel_awards.append(tagH)
    except:
        pass
    return hotel_awards


def hotelPress(website):
    print(website['id'])
    print(website['domain'])
    soup = webdriver(website['domain'])
    searchItems = ['press', 'basin', 'haber', 'news']
    hotel_press = []
    for tag in soup.find_all('a'):
        try:
            tagText = tag.get_text()
            if len(tagText) > 0:
                tagRaw = unidecode(str(tagText).lower())
                if 'newsletter' not in tagRaw and any(x in tagRaw for x in searchItems):
                    hotel_press.append(tag)
        except:
            pass
    return hotel_press


def hotelConsent(website):
    print(website['id'])
    print(website['domain'])
    searchItems = ['accept', 'kabul', 'anladim',
                   'consent', 'agree', 'submit', 'onay']
    hotel_consent = []
    soup = webdriver(website['domain'])
    try:
        for tag in soup.find_all(['a', 'button']):
            try:
                tagText = tag.get_text()
                if len(tagText) > 0:
                    tagRaw = unidecode(str(tagText).lower())
                    if any(x in tagRaw for x in searchItems):
                        hotel_consent.append(tag)
            except:
                pass
        for tag in soup.find_all('div'):
            try:
                if tag.get('class') == 'button':
                    tagText2 = tag.get_text()
                    tagText2 = unidecode(str(tagText2).lower())
                    if any(x in tagText2 for x in searchItems):
                        hotel_consent.append(tag)
            except:
                pass

    except:
        pass
    return hotel_consent


def hotelCovid(website):
    print(website['id'])
    print(website['domain'])
    searchItems = [['covid'], ['pandemi'], [
        'guvenli', 'turizm'], ['safe', 'tourism']]
    hotel_covid = []
    soup = webdriver(website['domain'])
    for tag in soup.find_all(['a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        tagRaw = unidecode(str(tag).lower())
        for i in searchItems:
            if all(x in tagRaw for x in i) and tag not in hotel_covid:
                hotel_covid.append(tag)

    return hotel_covid


def hotelApp(website):
    print(website['id'])
    print(website['domain'])
    tagArray = []
    searchItems = [['google', 'play'], ['app', 'store']]
    searchApps = ['apps.apple.com', 'play.google.com']
    hotel_app = []
    soup = webdriver(website['domain'])
    for tag in soup.find_all(['a', 'button']):
        try:
            tagRaw = unidecode(str(tag).lower())
            for search in searchItems:
                if all(x in tagRaw for x in search):
                    tagArray.append(tag)
        except:
            pass
    if len(tagArray) > 0:
        for tag in tagArray:
            if '<a' in str(tag):
                text = tag.get('href')
                tag1 = 'a'
                cName = 'href'

            elif '<button' in str(tag):
                tag1 = 'button'
                if tag.get('id') != None:
                    text = tag.get('id')
                    cName = 'id'
                elif tag.get('class') != None:
                    text = ' '.join(tag.get('class'))
                    cName = 'class'
            try:
                xpath = f'//{tag1}[@{cName}="{text}"]'
                url = xpathclick(website['domain'], xpath)
                if any(x in str(url) for x in searchApps):
                    hotel_app.append(url)
                    print(url)
            except:
                continue

            if len(hotel_app) > 0:
                break
            else:
                continue

    return hotel_app


def hotelSecure(website):
    print(website['id'])
    print(website['domain'])
    searchItems = ['https']
    hotel_secure = []
    if any(x in website['domain'] for x in searchItems):
        hotel_secure.append(website['domain'])
    return hotel_secure


def hotelLiveSup(website):
    print(website['id'])
    print(website['domain'])
    searchItems = ['wa.me', 'api.whatsapp']
    searchItems2 = ['join', 'chat']
    hotel_livesup = []
    soup = webdriver(website['domain'])
    for tag in soup.find_all(['a', 'button']):
        try:
            tagRaw = unidecode(str(tag).lower())
            if any(x in tagRaw for x in searchItems):
                hotel_livesup.append(tag)
            else:
                for tag in soup.find_all('div'):
                    clas = tag.get('class')
                    if all(x in clas for x in searchItems2):
                        hotel_livesup.append(tag)

        except:
            pass
    return hotel_livesup


def hotelSocial(website):
    print(website['id'])
    print(website['domain'])
    searchItems = ['instagram', 'facebook', 'twitter']
    errorMessages = ['busayfayaulasilamiyor',
                     'thispageisntavailable', 'thisaccountdoesntexist']
    hotel_social = []
    soup = webdriver(website['domain'])
    sayac = 0
    for tag in soup.find_all('a'):
        try:

            href = tag.get('href')
            if any(x in str(href).lower() for x in searchItems):
                href = str(href)
                soup2 = webdriver(href)
                for tag2 in soup2.find_all(['h2', 'span']):
                    tagText = tag2.get_text()
                    tagText = str(tagText)
                    text = ''
                    for i in tagText:
                        if i.isalpha():
                            text += i
                    if any(x in text for x in errorMessages):
                        sayac += 1
                if sayac == 0:
                    hotel_social.append(href)
                # xpath = f'//a[@href[1] = "{href}"] | //a[@href[2] = "{href}"]'
                # url = xpathclick(domain, xpath)
        except:
            pass
        if len(hotel_social) > 0:
            break
        else:
            continue

    return hotel_social


def hotelActiv(website):
    print(website['id'])
    print(website['domain'])
    searchItems = ['activit', 'hizmet', 'deneyim',
                   'aktivite', 'services', 'olanak', 'imkan', 'amenit']
    hotel_activ = []
    soup = webdriver(website['domain'])
    for tag in soup.find_all(['a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        try:
            tagT = tag.get_text()
            tagT = unidecode(str(tag).lower())
            if any(x in tagT for x in searchItems):
                hotel_activ.append(tag)
        except:
            pass
    return hotel_activ


def hotelSearch(website):
    print(website['id'])
    print(website['domain'])
    searchItems = ['search']
    hotel_search = []

    soup = webdriver(website['domain'])

    for tag in soup.find_all('input'):
        try:
            tagType = tag.get('type')
            if len(tagType) > 0:
                tagText = unidecode(str(tag).lower())
                if tagType != None and str(tagType) == 'text':
                    if any(x in tagText for x in searchItems):
                        hotel_search.append(tag)
        except:
            pass
    return hotel_search


def hotelTrip(website):
    print(website['id'])
    print(website['domain'])
    searchItems = ['www.tripadvisor']
    hotel_trip = []
    soup = webdriver(website['domain'])
    for tag in soup.find_all('a'):
        try:
            tagRaw = unidecode(str(tag).lower())
            tagHref = tag.get('href')
            if any(x in str(tagRaw) for x in searchItems):
                try:
                    if statuscode(tagHref) == 200:
                        hotel_trip.append(tagHref)
                except:
                    pass
        except:
            pass
    return hotel_trip


def hotelPrice(website):
    print(website['id'])
    print(website['domain'])
    searchItems = [['fiyat', 'garanti'], ['best', 'price'], ['low', 'price']]
    hotel_price = []
    soup = webdriver(website['domain'])
    for tag in soup.find_all(['img', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'a']):
        try:
            tagRaw = unidecode(str(tag).lower())
            for i in searchItems:
                if all(x in tagRaw for x in i):
                    hotel_price.append(tag)
            if hotel_price > 0:
                break
            else:
                continue
        except:
            pass
    return hotel_price
