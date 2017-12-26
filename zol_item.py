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
import numpy as np

'''
###Grab all the 100 pages###
'''
#page_collect=['https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&IsNodeId=1&N=100019096%20600014652%2050001146%2050001186%2050001315%2050010418%2050010772%2050034050%2050093120%2050118564']
page_collect=[]
for i in range(1,6):
    page='http://detail.zol.com.cn/desktop_pc/acer_alienware/'+str(i)+'.html'
    page_collect.append(page)

url_collect=[]

split1=np.arange(45)
split2=np.split(split1,9)+[range(45,49)]
for h in range(len(split2)):
    for k in split2[h]:
        page=page_collect[k]
    #newegg_laptop=requests.get(page,proxies=proxies)
        zol_laptop=requests.get(page)
        c_zol_laptop=zol_laptop.content
        soup_zol_laptop=BeautifulSoup(c_zol_laptop,"html.parser")
        #zol_laptop_urlall=soup_zol_laptop.findAll('div',{"class":"pro-intro"})
        url=[item.find('a').get('href') for item in soup_zol_laptop.findAll('div',{"class":"pro-intro"})]
        url_collect.append(url)
        time.sleep(random.randrange(1,5))
    time.sleep(random.randrange(300,480))

url_collect_set=set(url_collect)
url_collect_list=list(url_collect_set) 	    
url_pool_http=[]
for url in url_collect_list:
    dig=re.findall('\d+',url)
    for i in dig:
        url_http='http://detail.zol.com.cn/'+str(int(i)//1000+1)+'/'+i+'/param.shtml'    
    url_pool_http.append(url_http)

for h in range(len(url_pool_http)):
    url=url_pool_http[h]   
    r_zol=requests.get(url,proxies=proxies)
    c_zol=r_zol.content
    soup_zol=BeautifulSoup(c_zol,"html.parser",from_encoding='gb18083')
    zol_1=soup_zol.findAll('div',attrs={'id': "paramTable"})   
    Feature_field=[]
    for feature in zol_1:
        Feature_field.append(feature.findAll('span',attrs={'id':re.compile('newPmName')}))
    Feature_field_1=[]
    for i in Feature_field:
        for j in i:
           Feature_field_1.append(j)
    Feature_field_2=[]
    for i in Feature_field_1:
        Feature_field_2.append(i.get_text())
    Feature_field_2.append('Model')
    Feature_value=[]
    for feature in zol_1:
        Feature_value.append(feature.findAll('span',attrs={'id':re.compile('newPmVal')}))
    Feature_value_1=[]
    for i in Feature_value:
        for j in i:        
            Feature_value_1.append(j)     
    Feature_value_2=[]
    for i in Feature_value_1:       
        Feature_value_2.append(i.get_text(strip=True))    
    model=soup_zol.findAll('div',attrs={'class': "section-param-header section-header"})
    for i in model:
        Feature_value_2.append(i.get_text(strip=True))
    dic=dict(zip(Feature_field_2,Feature_value_2)) 
    total_output.append(dic)
    time.sleep(random.randrange(1,5))
    with open('zol_tdt_item.json', 'w') as f:
        json.dump(total_output, f)

		
with open('zol_tdt_item.json', 'r') as f:
     zol_item=json.load(f)

brand=['lenovo' , 'thinkpad' , 'asus' , 'acer' , 'hp' , 'dell' , '联想' , '戴尔' , '惠普' , '宏碁', '华硕']
jd_item_main=[]
for item in jd_item:
    try:
        value=item['sku-name'].lower()
        if(any([i in value for i in brand])==True):
            jd_item_main.append(item)    
    except (KeyError):
        next
zol_main_dic=[dict(t) for t in set(tuple(d.items()) for d in zol_item)]   

features_pool=[]
for item in zol_main_dic:
    key=list(item.keys())
    for i in key:
        features_pool.append(i)
s_pool=set(features_pool)
l_pool=list(s_pool)  

data_frame=pd.DataFrame([],columns=l_pool)
for item in zol_main_dic:
    data_frame=data_frame.append(item,ignore_index=True)    
data_frame_v1=pd.DataFrame([],columns=l_pool)    
    
data_frame_v1.to_csv('zol_item.csv',sep=',',encode='utf-8-sig')  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    