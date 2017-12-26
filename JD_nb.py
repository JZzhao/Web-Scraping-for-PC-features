# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 16:47:58 2017

@author: fremont_zhao
"""

from bs4 import BeautifulSoup
import requests
import time
import random
import csv
import json
import numpy as np

'''
###Grab all pages###
'''
page_collect=[]
for i in range(1049):
    page='https://list.jd.com/list.html?cat=670,671,672&page='+ str(i)+'&sort=sort_totalsales15_desc&trans=1&JL=6_0_0#J_main'
    page_collect.append(page)

for page in page_collect:
    jd_laptop=requests.get(page)
    c_jd_laptop=jd_laptop.content
    soup_jd_laptop=BeautifulSoup(c_jd_laptop,"html.parser",from_encoding='utf-8')    
    for item in soup_jd_laptop.findAll('div',{"class":"p-name"}):
        url=item.find('a').get('href')
        url_collect.append(url)

url_collect_set=set(url_collect)
url_collect_list=list(url_collect_set) 		
url_pool_http=[]
for url in url_collect_list:
    for i in url:
		url_http='https:'+i
		url_pool_http.append(url_http)

'''
###Crawl data from pages###
'''	
total_output=[]
item_overseas=[]	
for url in url_pool_http:
    try:
        r_jd=requests.get(url)
        c_jd=r_jd.content
        soup_jd=BeautifulSoup(c_jd,"html.parser",from_encoding='gb18083')
        jd_1=soup_jd.findAll('div',attrs={'class': "Ptable-item"})
    except AttributeError:
        item_overseas.append(url)##pages with JD overseas items are of different structure, which we don't need crawl
        next
    Feature_field=[]
    for feature in jd_1:
        Feature_field.append(feature.findAll('dt'))
    Feature_field_1=[]
    for i in Feature_field:
        for j in i:
           Feature_field_1.append(j)
    Feature_field_2=[]
    for i in Feature_field_1:
        Feature_field_2.append(i.get_text())
    Feature_field_2.append('sku-name')
    Feature_value=[]
    for feature in jd_1:
        Feature_value.append(feature.findAll('dd'))
    Feature_value_1=[]
    for i in Feature_value:
        for j in i:        
            Feature_value_1.append(j) 
    trash=[]
    for i in Feature_value_1:
       paragraphs = i.find_all('p')
       for paragraph in paragraphs:
           j=paragraph.get_text(strip=True)
           trash.append(j)
    Feature_value_2=[]
    for i in Feature_value_1:       
        h=i.get_text(strip=True)
        if h not in trash and len(h)>0:
            Feature_value_2.append(h)    
    sku=soup_jd.findAll('div',attrs={'class': "sku-name"})
    for i in sku:
        Feature_value_2.append(i.get_text(strip=True))
    dic=dict(zip(Feature_field_2,Feature_value_2))
    if len(dic)==1:
        item_overseas.append(url)
    else:
        total_output.append(dic)

with open('jd_item.json', 'w') as f:
     json.dump(total_output, f)
'''
###covert json file into dataframe and save into csv file###
'''
with open('jd_item.json', 'r') as f:
     jd_item=json.load(f)
###keys are too messed up, thus only keep main brands
brand=['lenovo' , 'thinkpad' , 'asus' , 'acer' , 'hp' , 'dell' , '联想' , '戴尔' , '惠普' , '宏碁', '华硕']
jd_item_main=[]
for item in jd_item:
    try:
        value=item['sku-name'].lower()
        if(any([i in value for i in brand])==True):
            jd_item_main.append(item)    
    except (KeyError):
        next
jd_main_dic=[dict(t) for t in set(tuple(d.items()) for d in jd_item_main)]

###decode and encode 
jd_main_dic_enc=[]
for item in jd_main_dic:
    key=list(item.keys())
    value=list(item.values())
    key_dec=[]
    value_dec=[]
    for i in key:
        try:
            i_enc=i.encode('latin-1')
            i_dec=i_enc.decode('gb2312')
        except (UnicodeDecodeError,UnicodeEncodeError):
            i_dec=i
        key_dec.append(i_dec)
    for j in value:
        try:
            j_enc=j.encode('latin-1')
            j_dec=j_enc.decode('gb2312')
        except (UnicodeDecodeError,UnicodeEncodeError):
            j_dec=j
        value_dec.append(j_dec)
    dic=dict(zip(key_dec,value_dec))
    jd_main_dic_enc.append(dic)
     
features_pool=[]
for item in jd_main_dic_enc:
    key=list(item.keys())
    for i in key:
        features_pool.append(i)
s_pool=set(features_pool)
l_pool=list(s_pool)  
    
data_frame=pd.DataFrame([],columns=l_pool)
for item in jd_main_dic_enc:
    data_frame_v1=data_frame.append(item,ignore_index=True)    
data_frame_v1.to_csv('jd_item.csv',sep=',',encode='utf-8-sig')   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    