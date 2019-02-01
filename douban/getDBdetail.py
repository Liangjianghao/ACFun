#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/10/3 23:59
# @Author : LiangJiangHao
# @Software: PyCharm
import os
import sys
import requests
from lxml import html
import pymysql
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import time
# CREATE TABLE `douban2018` (
#   `Id` INT(11) NOT NULL AUTO_INCREMENT,
#   `title` VARCHAR(255) DEFAULT NULL COMMENT '电影名',
#   `directors` VARCHAR(255) DEFAULT NULL COMMENT '导演',
#   `rate` FLOAT DEFAULT NULL COMMENT '评分',
#   `url` VARCHAR(255) DEFAULT NULL COMMENT '地址',
#   `idnumber` INT(11) DEFAULT NULL COMMENT 'idnumber',
#   `date` DATE DEFAULT NULL COMMENT '上映日期',
#   `type` VARCHAR(255) DEFAULT NULL COMMENT '类型',
#   PRIMARY KEY (`Id`)
# ) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COMMENT='豆瓣2018';

connect = pymysql.Connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='123456',
    db='douban',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor

)
cursor = connect.cursor()


def getUptime(url):
    url = 'https://movie.douban.com/subject/30337185/'
    response = requests.get(url, verify=False).content
    print(response)
    selector = html.fromstring(response)
    typeSelect = selector.xpath('//*[@id="info"]/span[4]/text()')
    # print(typeSelect[0])
    type=typeSelect[0]
    productInfo = selector.xpath('//*[@id="info"]/span[8]/text()')
    uptime = productInfo[0].split('(')[0]
    # print(len(productInfo))
    print(uptime)
    return type,uptime

with open('2018movie.txt',encoding='utf-8') as file:
    data=file.readlines()
print(len(data))
for index,video in enumerate(data):
    if index==1:
        break
    try:
        print('正在解析第%s条电影数据'%str(index+1))
        arr=video.split('----')
        print(arr)
        title=arr[0]
        directors=arr[2]
        idnumber=arr[3]
        url=arr[4]
        rate=arr[1]
        type,uptime=getUptime(url)
        # print(type,uptime)
        sql = 'insert into douban2018 (title,directors,rate,url,idnumber,date,type)values ("%s","%s","%s","%s","%s","%s","%s")' % (title,directors,rate,url,idnumber,uptime,type)
        print(sql)
        cursor.execute(sql)
        connect.commit()
        time.sleep(3)
    except Exception as e:
        print(e)
        continue


