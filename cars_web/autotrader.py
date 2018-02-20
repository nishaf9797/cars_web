import os, sys, django
sys.path.append("/home/nishaf/PycharmProjects/Upwork_Projects")  # here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cars_web.settings")
django.setup()

import requests
from bs4 import BeautifulSoup
from cars_web.models import CarsDetails
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

#proxy = {'http': '173.202.203.15:38990', 'https': '173.202.203.15:38990'}
proxy = {'http': '191.252.120.235:3128', 'https': '191.252.120.235:3128'}
#proxy = {'http': '71.49.153.49:13254', 'https': '71.49.153.49:13254'}
#proxy = {'http': '78.174.139.110:8080', 'https': '78.174.139.110:8080'}
#proxy = {'http': '212.48.85.164:3128', 'https': '212.48.85.164:3128'}
headers = {'User-agent': 'Safari/537.36'}


def save_data(website, make, model, title, link):
    CarsDetails(website=website,make=make, model=model, title=title, link=link).save()

def delete_previous_results(website, make, model):
    if CarsDetails.objects.filter(website=website, make=make, model=model).count() > 0:
        CarsDetails.objects.filter(website=website, make=make, model=model).all().delete()


def get_auto_trader_data(make, model, min_year, max_year):
    delete_previous_results('autotrader.com', make, model)
    print('Retrieving Results....')
    url = 'https://www.autotrader.com/cars-for-sale/'
    url_changed = url + make + "/" + model + "/?startYear=" +min_year+ "&endYear=" + max_year + "&numRecords=100"
    print(url_changed)
    data = requests.get(url_changed, headers=headers, proxies=proxy)
    print(data.status_code)
    soup = BeautifulSoup(data.text)
    premium_listing = soup.find_all('div', attrs={'data-qaid': 'cntnr-lstng-premium'})
    listing = premium_listing + soup.find_all('div', attrs={'data-qaid': 'cntnr-lstng-featured'})
    if soup.find('strong', attrs={'class': 'text-xlg text-normal'}) is not None:
        print("No Data Found")
        return

    for i in listing:
        title_data = i.find('a', attrs={'class': 'text-md'})
        title = title_data.text.strip()
        link = "https://www.autotrader.com" + title_data.get('href')
        print(title, link)
        save_data('autotrader.com', make, model, title, link)

#get_auto_trader_data('Acura','Integra', '1981','2016')

def get_cars_data(make_id, made_id):
    print(make_id, made_id)
    url1 = 'https://www.cars.com/for-sale/searchresults.action/?mdId=55767&mkId=33583&page=1&perPage=100' #'https://www.cars.com/for-sale/searchresults.action?mkId='+ str(make_id) + '&mdId='+str(made_id)+'&page=1&perPage=100&&zc='
    print('Loading Data....')
    data = requests.get(url1, headers=headers, proxies=proxy, verify=False)
    soup = BeautifulSoup(data.text)
    listing = soup.find_all('div', attrs={'class': 'shop-srp-listings__listing'})
    print(len(listing))
    for item in listing:
        title_data = item.find('h2', attrs={'class': 'cui-delta listing-row__title'})
        title = title_data.text.strip()
        link =  "https://www.cars.com/" + (title_data.find('a')).get('href')
        #save_data(title, link)
        print("Title: " + title)
        print("Link: https://www.cars.com/" +link)
        print("====================")

def get_carsforsale_data(make, model, years):
    delete_previous_results('carsforsale.com', make, model)
    url1 = 'https://www.carsforsale.com/Search?Make=' + str(make) +'&Model='+ str(model) +'&MinModelYear=' + str(years) + '&ZipCode=&Radius=100&PageNumber=1'
    print('Loading Data....')
    print(url1)
    data = requests.get(url1, headers=headers)
    soup = BeautifulSoup(data.text)
    #print(soup.prettify())

    listing = soup.find_all('li', attrs={'class': 'vehicle-thumb col-xs-12 vehicle-list vehicle-results-snapshot'})

    for item in listing:
        title = item.find('h4', attrs={'itemprop': 'name'}).text.strip()
        link = "https://www.carsforsale.com/" + (item.find('a', attrs={'class': 'vehicle-name vehicle-details-navigate'})).get('href')
        save_data('carsforsale.com', make, model,title, link)
        print("Title: " + title)
        print("Link: https://www.carsforsale.com/" + link)
        print("====================")


#get_carsforsale_data('Acura','Integra', '1981')
#get_cars_data(33583, 55767)
#get_auto_trader_data()
#get_cars_data()

'''
url = "https://www.autotrader.com"
PROXY = '51.15.35.239:3128'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)
driver = webdriver.Chrome('/home/nishaf/chromedriver', chrome_options=chrome_options)
driver.get(url)
#data = requests.get(url, headers=headers, proxies=proxy)
try:
    dialog = driver.find_element_by_xpath("//body[@class='modal-open']")
    dialog.send_keys(Keys.ESCAPE)
    sleep(1)
except:
    pass
make = driver.find_element_by_xpath("//select[@name='makeCodeListPlaceHolder']")
make.click()
for i in make.find_elements_by_xpath("//option"):
    if str(i.text).lower() == 'acura':
        i.click()

sleep(0.5)
make = driver.find_element_by_xpath("//select[@name='modelCodeListPlaceHolder']")
make.click()
for i in make.find_elements_by_xpath("//option"):
    if str(i.text).lower() == 'integra':
        i.click()

sleep(0.5)
driver.find_element_by_xpath("//input[@name='zip']").send_keys("99524")
sleep(10)
driver.find_element_by_xpath("//button[@class='btn btn-primary btn-block']").click()
sleep(10)
'''