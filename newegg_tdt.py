# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 16:47:58 2017

@author: fremont.zhao
"""
from bs4 import BeautifulSoup
import requests
import time
import random
import http.client
import csv
import json

'''
Grab all the url in 100 pages
'''
page_collect=['https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&IsNodeId=1&N=100019096%20600014652%2050001146%2050001186%2050001315%2050010418%2050010772%2050034050%2050093120%2050118564']
for i in range(100):
    page='https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&N=100019096%20600014652%2050001146%2050001186%2050001315%2050010418%2050010772%2050034050%2050093120%2050118564&IsNodeId=1&bop=And&Page='+str(i)+'&PageSize=36&order=BESTMATCH'
    page_collect.append(page)

url_collect=[]
for page in page_collect:    
    newegg_laptop=requests.get(page)
    c_newegg_laptop=newegg_laptop.content
    soup_newegg_laptop=BeautifulSoup(c_newegg_laptop,"html.parser")
    newegg_laptop_urlall=soup_newegg_laptop.findAll('div',{"class":"item-info"})
    url=[item.find('a',{"class":"item-title"}).get('href') for item in soup_newegg_laptop.findAll('div',{"class":"item-info"})]
    url_collect.append(url)
    time.sleep(random.randrange(1,5))# Break time ranges 1~5 seconds between each approach

url_collect_tdt=[] 
for i in url_collect:
    for j in i:
        url_collect_tdt.append(j)
 
'''Remove duplicated url'''
spool=set(url_collect_tdt)
lpool=list(spool)
url_pool_dis=lpool

''''''''''''''''''''''''''''''
'''Crawl items from the url'''  
''''''''''''''''''''''''''''''

###In case that the crawler is blocked by newegg
###We Crawl 30 pages every time and rest for about 5 mins
'''split url_pool into 62 lists'''
split1=np.arange(1830)
split2=np.split(split1,61)+[range(1830,1872)]
'''Crawl and save into json file'''
total_output=[]
for h in range(len(split2)):
    for k in split2[h]:        
        url=url_pool_dis[k]
        try:
            r_newegg=requests.get(url)#proxies=proxies)
        except AttributeError:
            next
        c_newegg=r_newegg.content
        soup_newegg=BeautifulSoup(c_newegg,"html.parser")
        newegg_1=soup_newegg.findAll('div',attrs={'id': "Specs"})
        Feature_field=[]
        for feature in newegg_1:
            Feature_field.append(feature.findAll('dt'))
        Feature_field_1=[]
        for i in Feature_field:
            for j in i:
               Feature_field_1.append(j)
        Feature_field_2=[]
        for i in Feature_field_1:
            Feature_field_2.append(i.get_text())
        Feature_value=[]
        for feature in newegg_1:
            Feature_value.append(feature.findAll('dd'))
        Feature_value_1=[]
        for i in Feature_value:
            for j in i:
               Feature_value_1.append(j) 
        Feature_value_2=[]
        for i in Feature_value_1:
            Feature_value_2.append(i.get_text())
        dic=dict(zip(Feature_field_2,Feature_value_2))
        total_output.append(dic)
        time.sleep(random.randrange(1,5))
    with open('newegg_tdt_item.json', 'w') as f:
        json.dump(total_output, f)## Save into json file
    time.sleep(random.randrange(300,480))
   
''''''''''''''''''''''''''''''''''''''''''''''''
'''Read from json file and save as data frame'''
''''''''''''''''''''''''''''''''''''''''''''''''
with open('newegg_tdt_item.json', 'r') as f:
     newegg_item = json.load(f)

newegg_item_dic=[dict(t) for t in set(tuple(d.items()) for d in newegg_item)]#remove duplicated item
newegg_item_dic[random.randrange(0,len(newegg_item_dic))]#randomly check the features of item

'''Get all unique features from keys'''
features_pool=[]
for item in newegg_item_dic:
    key=list(item.keys())
    for i in key:
        features_pool.append(i)
s_pool=set(features_pool)
l_pool=list(s_pool)   

'''convert into dataframe'''    
data_frame=pd.DataFrame(columns=l_pool)
for item in newegg_item_dic:
    data_frame=data_frame.append(item,ignore_index=True)

us_manual=pd.read_csv('newegg_tdt_item.csv')    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    