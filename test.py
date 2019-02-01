#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/8/30 15:41
# @Author : LiangJiangHao
# @Software: PyCharm
import os
import sys
import requests
import json
import time

timeStamp = str(1529486127000)[:-3]
print(timeStamp)
timeArray = time.localtime(int(timeStamp))
print(timeArray)
otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
print(otherStyleTime)
time.sleep(1000)
def returnId(idStr):
    header_dict = {'deviceType': '0', 'market': 'appstore', 'appVersion': '4.7.6','udid':'E8131C7D-8AD5-45A0-8E6A-5F97A90CA5A9'}
    url = "https://apipc.app.acfun.cn/v2/videos/%s" % idStr
    # print(url)
    res = requests.get(url, headers=header_dict).content
    result = json.loads(res)
    print(result)
    f=open('1.txt','wb+')
    f.write(res)
    f.close()
    # print(result['vdata']['videos'][0]['videoId'])
    # return result['vdata']['videos'][0]['videoId']
    # return str(result['vdata']['channelId']) + '-' + str(result['vdata']['parentChannelId'])
    return str(result['vdata']['parentChannelId']) + '-' + str(result['vdata']['channelId'])

def getType():
    with open('type.json',encoding='utf-8') as jsondata:
        jsonDic=json.load(jsondata)
    typeArr=jsonDic['vdata']['video']
    print(len(typeArr))
    dic = {}
    for type in typeArr:
        detailArr=type['children']
        type_one=type['name']
        for detail in detailArr:
            pid=detail['pid']
            id=detail['id']
            type_two=detail['name']
            dic[str(pid)+'-'+str(id)] = type_one+'-'+type_two
    print(dic)
    with open("acType.json","w") as f:
        json.dump(dic,f)
        # print("加载入文件完成...")
    print('写入文件')

with open('acType.json',encoding='utf-8') as f:
    typeDic=json.load(f)
print(typeDic)

# print(returnId(acid))
# danmuID=returnId(acid)
# danmuUrl = 'http://danmu.aixifan.com/V4/%s/0/500' % danmuID
# # print(danmuUrl)
# response = requests.get(danmuUrl).content
# jsonData = json.loads(response)
# for danmu in jsonData:
#     if len(danmu) > 0:
#         for dm in danmu:
#             print(dm['m'])

# response=requests.get(url).content
# # print(response)
# f.write(response)

# f.close()
