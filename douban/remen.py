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

type='热门'
page=1
startTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
f=open('rm.txt','w+',encoding='utf-8')
while 1:
    print('正在抓取第%s页'%page)
    dmUrl='https://movie.douban.com/j/search_subjects?type=movie&tag=%s&sort=recommend&page_limit=20&page_start=%s'%(type,page*20)
    print(dmUrl)
    response=requests.get(dmUrl).content
    jsondata=json.loads(response)
    dmArr=jsondata['subjects']
    # print(dmArr[0])
    if len(dmArr)==0:
        break
    for dm in dmArr:
        title=dm['title']
        # directorsArr=dm['directors']
        # if len(directorsArr)>0:
        #     directors=directorsArr[0]
        # else:
        #     directors='无'
        url=dm['url']
        id=dm['id']
        rate=dm['rate']
        print(title)
        f.write(title+'----'+rate+'----'+id+'----'+url+'\n')
    page+=1
f.close()
endTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#现在
print ('开始：%s\n结束：%s\n'%(startTime,endTime))
