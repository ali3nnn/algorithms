import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import os

class AdStoria:
  def __init__(self, category='', state='', link='', price='', areaC='', areaU='', areaT='', rooms='', bathrooms='', floor='', maxFloor='', year='', partitioning='', orientation='', location=''):
    self.link = link
    self.price = price
    self.areaC = areaC
    self.areaU = areaU
    self.areaT = areaT
    self.rooms = rooms
    self.category = category
    self.state = state
    self.floor = floor
    self.maxFloor = maxFloor
    self.year = year
    self.bathrooms = bathrooms
    self.partitioning = partitioning
    self.orientation = orientation
    self.location = location

urlList = ['https://www.storia.ro/inchiriere/bucuresti/?nrAdsPerPage=72']
for i in range(2,168):
    urlList.append('https://www.storia.ro/inchiriere/bucuresti/?nrAdsPerPage=72&page='+str(i))

adListRaw = []
for index, url in enumerate(urlList):

    req = requests.get('https://www.storia.ro/inchiriere/bucuresti/?nrAdsPerPage=72')
    adCounter = 1
    if req.status_code == 200:
        soup = BeautifulSoup(req.content, features="html.parser")
        for ad in soup.find_all('article', attrs={"class": "offer-item"}):
            quickDetailsRaw = ad.find('div', {'class': 'offer-item-details'})
            headerRaw = quickDetailsRaw.find('header', {'class': 'offer-item-header'}).find('p', {
                    'class': 'text-nowrap'})

            try:
                category = headerRaw.get_text().split(' ')[0]
            except:
                category = 0

            try:
                location = headerRaw.get_text().split(':')[1]
            except:
                location = 0

            try:
                rooms = quickDetailsRaw.find('li', {'class': 'offer-item-rooms'}).get_text().split(' ')[0]
            except:
                rooms = 0

            try:
                areaC = quickDetailsRaw.find('li', {'class': 'offer-item-area'}).get_text().split(' ')[0]
            except:
                areaC = 0

            try:
                price = quickDetailsRaw.find('li', {'class': 'offer-item-price'}).get_text().split('/luna')[0].replace(
                    " ", "").replace("\n", "").replace("~", "")
            except:
                price = 0

            adEl = AdStoria(link=ad['data-url'], category=category, location=location, price=price, areaC=areaC,
                            rooms=rooms)

            adPage = requests.get(adEl.link)
            print(index+1,'/',len(urlList), adCounter, adPage.status_code, adEl.link)
            adCounter = adCounter + 1

            if adPage.status_code == 200:
                adPageParser = BeautifulSoup(adPage.content, features="html.parser")

                try:
                    deatiledDesc = adPageParser.find('section', {"class": "section-overview"})

                    for detail in deatiledDesc.find_all('li'):
                        if "construit" in detail.get_text():
                            adEl.areaC = detail.find("strong").get_text()
                            continue
                        if "total" in detail.get_text():
                            adEl.areaT = detail.find("strong").get_text()
                            continue
                        if "camere" in detail.get_text():
                            adEl.rooms = detail.find("strong").get_text().split(" ")[0]
                            continue
                        if "utila" in detail.get_text():
                            adEl.areaU = detail.find("strong").get_text()
                            continue
                        if "constructiei" in detail.get_text():
                            adEl.year = detail.find("strong").get_text()
                            continue
                        if "Compartimentare" in detail.get_text():
                            adEl.partitioning = detail.find("strong").get_text()
                            continue
                        if "proprietate" in detail.get_text():
                            adEl.category = detail.find("strong").get_text()
                            continue
                        if "Etaj" in detail.get_text():
                            adEl.floor = detail.find("strong").get_text()
                            continue
                        if "total de etaje" in detail.get_text():
                            adEl.maxFloor = detail.find("strong").get_text()
                            continue
                        if "Numarul de bai" in detail.get_text():
                            adEl.bathrooms = detail.find("strong").get_text().split(" ")[0]
                            continue
                        if "Stare" in detail.get_text():
                            adEl.state = detail.find("strong").get_text()
                            continue
                except:
                    print("ERROR adEl")
            else:
                print("ERROR ADPAGE:", req.status_code)

            adListRaw.append(adEl)
    else:
        print("ERROR:", req.status_code)

adFrame = pd.DataFrame([o.__dict__ for o in adListRaw])
adFrame.to_excel(os.getcwd()+"/storia.xlsx", sheet_name='bucuresti')