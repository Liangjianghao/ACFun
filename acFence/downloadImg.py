#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/12/29 17:52
# @Author : LiangJiangHao
# @Software: PyCharm

import os
import sys
import requests
import pymysql
import urllib

connect = pymysql.Connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='123456',
    db='ac_up',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor

)
cursor = connect.cursor()
def selectData():
    # 连接数据库
    sql='SELECT *FROM up_baseInfor '
    cursor.execute(sql)
    data=cursor.fetchall()
    return data

print('getArr')
listArr=selectData()
print(len(listArr))
imgPath ='F:\ACimg'
if os.path.exists(imgPath):
    print('存在')
else:
    os.mkdir(imgPath)
for index,item in enumerate(listArr):
    if index<560000:
        continue
    try:
        userId=item['userid']
        imgUrl=item['userImg']
        if imgUrl=='http://cdn.aixifan.com/dotnet/20120923/style/image/avatar.jpg':
            continue
        userName=item['user_name']
        print('正在下载第%s张图片：%s'%(userId,userName))
        coverPath = '%s/%s.jpg' % (imgPath, userId)
        urllib.request.urlretrieve(imgUrl, coverPath)
    except Exception as e:
        print(e)
        continue

# http://cdn.aixifan.com/dotnet/20120923/style/image/avatar.jpg