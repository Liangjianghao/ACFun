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
	return result['vdata']['videos'][0]['videoId']

url = 'http://www.acfun.cn/v/ac4537807'
id = url.split('/ac')[1]
danmuID=returnId(id)
danmuUrl='http://danmu.aixifan.com/V4/%s/0/500'%danmuID
response=requests.get(danmuUrl).content
jsonData=json.loads(response)
for danmu in jsonData:
    if len(danmu) > 0:
        print(danmuUrl)
        for dm in danmu:
            print(dm['m'])





