#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/2 12:59
# @Author : LiangJiangHao
# @Software: PyCharm

import os
import requests
import json
def returnId(idStr):
    header_dict = {'deviceType': '0', 'market': 'appstore', 'appVersion': '4.7.6','udid':'E8131C7D-8AD5-45A0-8E6A-5F97A90CA5A9'}
    url = "https://apipc.app.acfun.cn/v2/videos/%s" % idStr
    # print(url)
    res = requests.get(url, headers=header_dict,verify=False).content
    result = json.loads(res)
    # print(result)
    # f=open('1.txt','wb+')
    # f.write(res)
    # f.close()
    # print(result['vdata']['videos'][0]['videoId'])
    return result['vdata']['videos'][0]['videoId']
    # return str(result['vdata']['channelId']) + '-' + str(result['vdata']['parentChannelId'])
    # return str(result['vdata']['parentChannelId']) + '-' + str(result['vdata']['channelId'])


dmFile=open('danmu.txt','w+',encoding='utf-8')
url='http://www.acfun.cn/v/ac4447301'
# url='http://www.acfun.cn/v/ac1282697_2'
url='http://www.acfun.cn/v/ac1282697'
url='http://www.acfun.cn/v/ac1758344'
acid = url.split('/ac')[1]
# print(returnId(acid))
danmuID=returnId(acid)
danmuUrl = 'http://danmu.aixifan.com/V4/%s/0/500' % danmuID
# print(danmuUrl)
response = requests.get(danmuUrl,verify=False).content
jsonData = json.loads(response)
print(jsonData)
for danmu in jsonData:
    if len(danmu) > 0:
        for dm in danmu:
            print(dm['m'])
            dmFile.write(dm['m']+'\n')
dmFile.close()
