#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/16 11:45
# @Author : LiangJiangHao
# @Software: PyCharm
import os
import sys
import random
import requests
import json

s= requests.Session()
url='http://www.acfun.cn/v/ac4585970'
s.get(url)
fanhao=url.split('/ac')[1]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}

cmUrl='http://www.acfun.cn/comment/list?isNeedAllCount=true&contentId=%s&currentPage=1'%fanhao
print(cmUrl)
#自动处理cookie
response=s.get(cmUrl).content
print(response)
jsonData=json.loads(response)
print(jsonData)
#response=requests.get(cmUrl,headers=headers).content
#print(response)


from selenium import webdriver

driver = webdriver.PhantomJS()
url = "https://et.xiamenair.com/xiamenair/book/findFlights.action?lang=zh&tripType=0&queryFlightInfo=XMN,PEK,2018-01-15"
driver.get(url)
# 获取cookie列表
cookie_list = driver.get_cookies()
# 格式化打印cookie
cookie_dict={}
for cookie in cookie_list:
    cookie_dict[cookie['name']] = cookie['value']
print(cookie_dict)
