"""
Created on Dec 26th 2017

@author: fremont.zhao
"""

**In this repo, I crawled PC features in https://www.newegg.com/ 
										 https://www.jd.com/ (Jingdong)
										 http://www.zol.com.cn/ (zhongguancun)
**First, we need crawl all the url links of PC items;
**Then, we scrape data of each item page based on specific rules;
**Web Scraping tool is BeautifulSoup package in Python;
**Programming environment is Python 3.5+, Windows 8.1 pro and Windows 10 pro;
**JD.com is dynamic website, and need decode and encode after grabbing data;
**Proxy service is deployed when crawler is blocked.