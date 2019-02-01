#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/8/17 15:09
# @Author : LiangJiangHao
# @Software: PyCharm
# -- coding: UTF-8 --
import requests
import json
import sys
from selenium import webdriver
import json
import time
def returnId(idStr):
	header_dict = {'deviceType':'0','market':'appstore','appVersion':'4.7.6'}
	res = requests.get("https://apipc.app.acfun.cn/v2/videos/%s"%idStr,headers=header_dict,verify=False).content
	result=json.loads(res)
	# print(result)
	# print(result['vdata']['videos'][0]['videoId'])
	return result['vdata']['videos'][0]['videoId']


# url = 'http://www.acfun.cn/v/ac4527112'
# id = url.split('/ac')[1]
# print(id)
# danmuID = returnId(id)
# UA = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.13 Safari/537.36"
# headers = {"User-Agent": UA, 'X-Requested-With': 'XMLHttpRequest'}
# danmuUrl = 'http://danmu.aixifan.com/V4/%s/0/500' % danmuID
# print(danmuUrl)
# response = requests.get(danmuUrl,headers=headers).content
# jsonData = json.loads(response)
# for danmu in jsonData:
#     if len(danmu)>0:
#         for dm in danmu:
#             print(dm['m'])
# time.sleep(10000)

with open('daceUrl.txt') as fileOpen:
    data=fileOpen.readlines()
print('需要解析%s条视频数据'%len(data))

f=open('暂停.txt','w+')
for index,url in enumerate(data):
    try:
        xrNum=0
        # url = 'http://www.acfun.cn/v/ac4527112'
        # print('正在解析第%s条视频数据：%s'%(str(index+1),url.strip()))
        id = url.split('/ac')[1]
        # print(id)
        danmuID=returnId(id)
        danmuUrl='http://danmu.aixifan.com/V4/%s/0/500'%danmuID
        # print(danmuUrl)
        response=requests.get(danmuUrl).content
        jsonData=json.loads(response)
        for danmu in jsonData:
            if len(danmu) > 0:
                print(danmuUrl)
                for dm in danmu:
                    if '暂停成功' in dm['m']:
                        print(dm['m'])
                        xrNum+=1
        if xrNum>0:
            # f.write(url.strip()+'----'+str(xrNum)+'\n')
            print('1')
    except Exception as e:
        print('跳过 %s'%e)
        continue
f.close()

