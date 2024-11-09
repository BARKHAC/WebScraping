import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from datascience import * 

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
site = "https://www.makaan.com/pune-residential-property/buy-property-in-pune-city?beds=2&propertyType=apartment&budget=0,5000000"


data = {
    'url': [],
    'area': [],
    'construction': [],
    'possess': [],
    'builderName': [],
    'cost': [],
    'suburb': [],
    'rooms': []   
    
}


#title = soup.title
#print(title.text)
def export_table_and_data(data):
    table = pd.DataFrame(data,columns=['url','area','construction','possess','builderName','cost','suburb','rooms'])
table.to_csv('properties1.csv',sep=',',encoding="utf-8")

def get_cd_attributes(cd):
    linky = cd.find('a',{'class':'projName'})['href']
    print(linky)
    sqft = cd.find('tr',{'class':'hcol'}).find('td',{'class':'lbl rate'}).text
    print(sqft)
    status = cd.find('tr',{'class':'hcol w44'}).find('td',{'class':'val'}).text
    print(status)
    #desc = cd.find('div',{'class':'listing-description'}).find('div',{'class':'txt'}).find('h3')
    #print(desc.text)
    poss = cd.find('ul',{'class':'listing-details'}).find('li',{'class':'keypoint'}).find('span').text #.find('strong').find('span')
    print(poss)
    s = cd.find('script',{'type':'text/x-config'}).string.strip()
    #print(s)
    dataa = json.loads(s)
    #print(dataa['builderName'])
    #print(dataa['price'])
    #print(dataa['suburbName'])
    #print(dataa['bedrooms'])
    data['url'].append(linky)
    data['area'].append(sqft)
    data['construction'].append(status)
    data['possess'].append(poss)
    data['builderName'].append(dataa['builderName'])
    data['cost'].append(dataa['price'])
    data['suburb'].append(dataa['suburbName'])
    data['rooms'].append(dataa['bedrooms'])

def parse_page(url):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page)
    links = soup.find_all('li',{'class':'cardholder'})
    print(len(links))
    for cd in links:
        get_cd_attributes(cd)
    
    npt = soup.find('div',{'class':'pagination'}).find('ul').find_all('li') #list of elements
    for nx in npt:
        if(nx.get("aria-label")=="nextPage"):
            dc = nx.find_all('a',{'aria-label':'nextPage'})
        #[-1]#['href']
        #['href'] 
        #print(dc)
    bb = dc.pop(-1)
    ac=bb["href"]
    print(ac)
    
    
    #ab = bb.find('a',{'aria-label':'nextPage'})['href']
    #print(ab)
    #.find_all('a')   #find_all('a',{'aria-label':'previous page'})['href']
    #print(next_page_text)
    export_table_and_data(data)
    
parse_page(site)

