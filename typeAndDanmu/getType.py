#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/2 12:59
# @Author : LiangJiangHao
# @Software: PyCharm

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
with open('test.txt') as file:
    data = file.readlines()
for url in data:
    try:
        acid=url.split('/ac')[1]
        typeID=returnId(acid)
        print('id:'+typeID)
        print(typeDic[typeID])
    except Exception as e:
        print(e)
        continue
    break
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
