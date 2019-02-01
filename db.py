#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/8/17 18:22
# @Author : LiangJiangHao
# @Software: PyCharm

# -*-coding:utf-8
import os
import sys
import requests
import re
import time
import pymysql
import datetime
import json
import pymysql.cursors

connect = pymysql.Connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='123456',
    db='acfun',
    charset='utf8mb4',
    cursorclass = pymysql.cursors.DictCursor
)
# 获取游标
cursor = connect.cursor()
# videoUrl,playNum,danmuNum,comments,saveNum,xjNum

selectStr='SELECT videoUrl FROM dance ORDER BY saveNum/playNum DESC limit 3'
descriStr='收藏/播放前三：'
f=open('final.txt','a+')
cursor.execute(selectStr)
connect.commit()
data = cursor.fetchall()
# print(data[0])
f.write(descriStr + '\n')
for video in data:
    print(video['videoUrl'])
    url='http://www.acfun.cn/v/ac%s'%video['videoUrl']
    f.write(url+'\n')
f.close()
