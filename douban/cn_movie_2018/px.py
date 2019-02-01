#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/3 19:41
# @Author : LiangJiangHao
# @Software: PyCharm
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/2 20:18
# @Author : LiangJiangHao
# @Software: PyCharm

import pymysql
import os
import sys
import time
import datetime
from dateutil import parser
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
baseTable='DB_cn_2018'
tableName='DB_cn_2018R'
baseTime='2018-1-1'
import json
# CREATE TABLE `DB_cn_2018R` (
#   `Id` INT(11) NOT NULL AUTO_INCREMENT,
#   `title` VARCHAR(255) NOT NULL COMMENT '电影名',
#   `movie_id` VARCHAR(255) DEFAULT NULL COMMENT '电影id',
#   `rate` FLOAT(11) DEFAULT NULL COMMENT'评分',
#   `url` VARCHAR(255) DEFAULT NULL COMMENT '网址',
#   `cover` VARCHAR(255) DEFAULT NULL COMMENT '封面',
#   `uploadTime` DATE DEFAULT NULL COMMENT '上映时间',
#   PRIMARY KEY (`Id`)
# ) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COMMENT='豆瓣2018中国电影结果';
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

def getinfor(timeStr):

    # sql = "SELECT * FROM %s  WHERE video_uploadtime<='%s' ORDER BY allPlayNum desc "%(baseTable,timeStr)
    sql='SELECT * FROM %s WHERE uploadTime<"%s" ORDER BY rate DESC LIMIT 20'%(baseTable,timeStr)
    print(sql)
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchall()
    return data

datetime_start = parser.parse(baseTime)
nowTime = datetime.datetime.now()  # 现在

while datetime_start<nowTime:
    datetime_start = datetime_start + datetime.timedelta(days=1)
    print('处理时间段%s'%(datetime_start))
    videoArr=getinfor(datetime_start)
    print(len(videoArr))
    for index,video in enumerate(videoArr):
        try:
            title = video['title']
            movie_id = video['movie_id']
            rate = video['rate']*10
            url = video['url']
            cover = video['cover']
            uploadTime = video['uploadTime']
            insertStr = "insert into %s (title,movie_id,rate,url,cover,uploadTime) values ('%s','%s', '%s','%s','%s','%s')" % (tableName,title, movie_id, rate, url, cover, datetime_start)
            cursor.execute(insertStr)
            connect.commit()
        except Exception as e:
            continue


