#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/8/29 12:46
# @Author : LiangJiangHao
# @Software: PyCharm
import pymysql
import os
import sys
import time
import datetime
from dateutil import parser

# CREATE TABLE `recent2` (
#   `Id` int(11) NOT NULL AUTO_INCREMENT,
#   `video_title` varchar(255) DEFAULT NULL COMMENT '视频标题',
#   `video_author` varchar(255) DEFAULT NULL COMMENT '视频作者',
#   `video_uploadtime` date DEFAULT NULL COMMENT'更新时间',
#   `playNum` int(11) DEFAULT NULL COMMENT '播放',
#   `allPlayNum` int(11) DEFAULT NULL COMMENT '总播放',
#   PRIMARY KEY (`Id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='a站最近总表2';
connect = pymysql.Connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='123456',
    db='acfun',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor

)
cursor = connect.cursor()
def getfort(timeStr):
    connect = pymysql.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='acfun',
        charset='utf8mb4',
        cursorclass = pymysql.cursors.DictCursor
    )
    cursor = connect.cursor()
    # sql = "SELECT *,sum(playNum) as allnumber FROM actable WHERE video_uploadtime<='%s' GROUP BY video_author ORDER BY allnumber desc limit 20"%timeStr
    newSql="SELECT *,SUM(playNum) AS allnumber FROM (SELECT * FROM actable WHERE video_uploadtime<='%s' ORDER BY id DESC  LIMIT 340000) t GROUP BY video_author ORDER BY allnumber DESC limit 20"%timeStr
    # print(sql)
    cursor.execute(newSql)
    connect.commit()
    data = cursor.fetchall()
    return data

baseTime='2017-9-26'
datetime_start = parser.parse(baseTime)

nowTime = datetime.datetime.now()  # 现在

while datetime_start<nowTime:
    datetime_start = datetime_start + datetime.timedelta(days=1)
    print('处理时间段%s'%(datetime_start))
    videoArr=getfort(datetime_start)
    print(len(videoArr))
    for index,video in enumerate(videoArr):
        video_title = video['video_title']
        video_author = video['video_author']
        video_uploadtime = str(video['video_uploadtime'])[0:10]
        playNum = video['playNum']
        allPlayNum = video['allnumber']
        sql = "insert into recent2(video_title,video_author,video_uploadtime,playNum,allPlayNum)values ('%s','%s', '%s','%s','%s')" % (video_title, video_author, datetime_start, playNum, allPlayNum)
        # print(sql)
        insertSql = "INSERT INTO recent2 (video_title,video_author,video_uploadtime,playNum,allPlayNum)SELECT '%s','%s','%s','%s','%s' FROM recent2 WHERE NOT EXISTS(SELECT video_author FROM recent2 WHERE video_author='%s' and video_uploadtime='%s')LIMIT 1" % (video_title, video_author, datetime_start, playNum, allPlayNum, video_author,datetime_start)
        # print(sql)
        if index==0:
            cursor.execute(sql)
        else:
            cursor.execute(insertSql)
        connect.commit()
    # break
