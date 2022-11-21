
# Library import.
import requests
from lxml.html import fromstring
from itertools import cycle
from bs4 import BeautifulSoup
import time
import random
import urllib.parse
import pygeohash as pgh


# Function to get a list of proxies. I am using only one proxy here.
# However, we can use multiple proxies to scrape large amount of data.
def ListOfProxies():

    # Source website URL.
    src = 'https://www.yelp.com/search?find_desc=&find_loc=Sydney%2C+New+South+Wales'

    # Website providing free proxies.
    response = requests.get('https://free-proxy-list.net/')
    parser = fromstring(response.text)
    proxies = set()
    ProxyList = []

    # Parsing the free proxy website.
    for i in parser.xpath('//tbody/tr'):
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0],
                              i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)

    # Add proxy to the list if works with the source website.
    if proxies:
        proxy_pool = cycle(proxies)
        for i in range(1, 25):
            proxy = next(proxy_pool)
            try:
                r = requests.get(src, proxies={"http": proxy, "https": proxy})
                file_request_succeed = r.ok

                if file_request_succeed:
                    print('Rotated IP %s succeed' % proxy)
                    ProxyList.append(proxy)
                    break
            except Exception as e:
                print('Rotated IP %s failed' % (proxy))

    return ProxyList


# scraping 100 restaurants from 10 webpages.
# The function accepts proxy as an argument.
def MakeRestaurantList(proxy):

    lr = []

    # Here we can use multiple proxies to not getting block from the website we are scrapping.
    # However, I am using only one proxy as the data to be scrapped is less.
    prox = {
        'http': 'http://' + proxy[0],
        'https': 'http://' + proxy[0]
    }

    for i in range(0, 100, 10):
        url = f'https://www.yelp.com/search?find_desc=&find_loc=Sydney%2C+New+South+Wales&start={i}'

        r = requests.get(url, proxies=prox)
        soup = BeautifulSoup(r.text, 'html.parser')

        restaurants_list = soup.find_all('div', {
            'class': 'padding-t3__09f24__TMrIW padding-r3__09f24__eaF7p padding-b3__09f24__S8R2d padding-l3__09f24__IOjKY border-color--default__09f24__NPAKY'})

        lr.append(restaurants_list)

        # Add buffer to scrape website gently.
        time.sleep(2)

    return lr


# Adding restaurant details (name, rating, URL) to a dictionary.
def AddingRestaurantDetails(listofres):

    main_di = []

    # Listofres is having 10 lists containing 10 restaurants each (as 1 yelp page contains 10 restaurants).
    for k in range(len(listofres)):
        for m in range(len(listofres)):
            dir = {}
            dir['restaurant_name'] = listofres[k][m].find('a', {'class': 'css-1m051bw'}).text
            dir['restaurant_url'] = 'https://www.yelp.com' + listofres[k][m].find('a', {'class': 'css-1m051bw'})[
                'href']
            restaurant_rating = listofres[k][m].find('div', {
                'class': 'five-stars__09f24__mBKym five-stars--regular__09f24__DgBNj display--inline-block__09f24__fEDiJ border-color--default__09f24__NPAKY'})[
                'aria-label']
            dir['restaurant_rating'] = float(restaurant_rating.split(' ')[0])
            main_di.append(dir)

    return main_di


# Adding price_type, address and review_highlights.
def AddingMoreFeatures(lisdict, proxy):
    dummy = list(range(len(lisdict)))

    # Sometimes proxies could not fetch the data and return an error.
    # So, this loop will make sure that we get all the restaurant data.
    while (len(dummy) > 0):

        i = random.choice(dummy)

        prox = {
            'http': 'http://' + proxy[0],
            'https': 'http://' + proxy[0]
        }

        try:

            html = requests.get(lisdict[i]['restaurant_url'], proxies=prox)
            soup = BeautifulSoup(html.text)

            if soup.find('span', {'class': 'css-1ir4e44'}) != None and '$' in soup.find('span',
                                                                                        {'class': 'css-1ir4e44'}).text:
                lisdict[i]['price_type'] = soup.find('span', {'class': 'css-1ir4e44'}).text
                lisdict[i]['price_type'] = lisdict[i]['price_type'].replace(' ', '')
            else:
                lisdict[i]['price_type'] = 'None'

            if soup.find('p', {'class': 'css-qyp8bo'}) != None:
                lisdict[i]['address'] = soup.find('p', {'class': 'css-qyp8bo'}).text
            else:
                lisdict[i]['address'] = 'None'

            fall = soup.find_all('p', {'class': 'css-2sacua'})
            hl = []

            for m in range(3):
                line = fall[m].text.split('”')[0]
                hl.append(line.replace('“',''))

            lisdict[i]['review_highlights'] = hl

            dummy.remove(i)

            time.sleep(2)

        except:
            pass

    return lisdict


# Adding geographic information(latitude, longitude, Geohash).
def AddingLocationFeatures(ListofDictionaries):

    for i in range(len(ListofDictionaries)):

        try:
            url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(ListofDictionaries[i]['address']) + '?format=json'

            response = requests.get(url).json()

            ListofDictionaries[i]['lat'] = response[0]["lat"]
            ListofDictionaries[i]['lon'] = response[0]["lon"]

            # Use precision=5 to locate restaurants within 5km radius.
            ListofDictionaries[i]['geohash'] = pgh.encode(response[0]["lat"], response[0]["lon"], precision=5)

        except:
            pass

    return ListofDictionaries