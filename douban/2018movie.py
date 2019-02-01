#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/10/3 20:05
# @Author : LiangJiangHao
# @Software: PyCharm
import os
import sys
import requests
import json
import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

type='电影'
page=20
startTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
f=open('2018movie.txt','w+',encoding='utf-8')
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.13 Safari/537.36"}
while 1:
    print('正在抓取第%s页'%str(page+1))
    dmUrl='https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%s&start=%s&year_range=2018,2018'%(type,page*20)
    print(dmUrl)
    response=requests.get(dmUrl,headers=headers,verify=False).content
    jsondata=json.loads(response)
    dmArr=jsondata['data']
    # print(dmArr[0])
    if len(dmArr)==0:
        break
    for dm in dmArr:
        title=dm['title']
        directorsArr=dm['directors']
        if len(directorsArr)>0:
            directors=directorsArr[0]
        else:
            directors='无'
        url=dm['url']
        id=dm['id']
        rate=dm['rate']
        print(title)
        if rate=='':
            rate=0
        f.write(title+'----'+str(rate)+'----'+directors+'----'+id+'----'+url+'\n')
    page+=1
f.close()
endTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#现在
print ('开始：%s\n结束：%s\n'%(startTime,endTime))
