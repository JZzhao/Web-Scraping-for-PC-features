# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 16:47:58 2017

@author: fremont_zhao
"""

from bs4 import BeautifulSoup

'''verify the proxy host'''
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "HO91B4A0E72Z96WD"
proxyPass = "4CD00F7486469AD4"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
  "host" : proxyHost,
  "port" : proxyPort,
  "user" : proxyUser,
  "pass" : proxyPass,
}

proxies = {
    "http"  : proxyMeta,
    "https" : proxyMeta,
}


'''
just for example
'''
page=['https://www.newegg.com/Laptops-Notebooks/SubCategory/ID-32?Tid=6740&PageSize=96&order=BESTMATCH']
jd_laptop=requests.get(page,proxies=proxies)
   



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    