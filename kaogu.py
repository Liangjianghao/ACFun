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


baseTable='actable'
tableName='ac_kaogu'
baseTime='2014-1-1'
fenTime='2007-6-20'
# CREATE TABLE `ac_kaogu` (
#   `Id` int(11) NOT NULL AUTO_INCREMENT,
#   `video_title` varchar(255) DEFAULT NULL COMMENT '视频标题',
#   `video_author` varchar(255) DEFAULT NULL COMMENT '视频作者',
#   `video_uploadtime` date DEFAULT NULL COMMENT'更新时间',
#   `playNum` int(11) DEFAULT NULL COMMENT '播放',
#   `allPlayNum` int(11) DEFAULT NULL COMMENT '总播放',
#   PRIMARY KEY (`Id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='a站考古总表';
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

def getinfor(timeStr):
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
    # sql = "SELECT *,sum(playNum) as allnumber FROM %s WHERE video_uploadtime<='%s' GROUP BY video_author ORDER BY allnumber desc limit 20"%(baseTable,timeStr)
    newSql="SELECT * FROM actable WHERE video_uploadtime>'%s' ORDER BY video_uploadtime LIMIT 20"%timeStr
    # newSql="SELECT * FROM (SELECT * FROM danceallzh  WHERE video_uploadtime<='%s' ORDER BY allPlayNum DESC LIMIT 15000) t GROUP BY video_author  ORDER BY allPlayNum DESC limit 20"%timeStr
    # print(sql)
    cursor.execute(newSql)
    connect.commit()
    data = cursor.fetchall()
    return data

datetime_start = parser.parse(baseTime)
datetime_start2 = parser.parse(fenTime)

nowTime = datetime.datetime.now()  # 现在

while datetime_start>datetime_start2:
    datetime_start = datetime_start + datetime.timedelta(days=-1)
    print('处理时间段%s'%(datetime_start))
    videoArr=getinfor(datetime_start)
    print(len(videoArr))
    for index,video in enumerate(videoArr):
        video_title = video['video_title']
        video_author = video['video_author']
        video_uploadtime = str(video['video_uploadtime'])[0:10]
        playNum = video['playNum']
        # allPlayNum = video['playNum']
        allPlayNum = 0

        sql = "insert into %s(video_title,video_author,video_uploadtime,playNum,allPlayNum)values ('%s','%s', '%s','%s','%s')" % (tableName,video_title, video_author, datetime_start, playNum, allPlayNum)
        # insertSql = "INSERT INTO %s (video_title,video_author,video_uploadtime,playNum,allPlayNum)SELECT '%s','%s','%s','%s','%s' FROM %s WHERE NOT EXISTS(SELECT video_author FROM %s WHERE video_author='%s' and video_uploadtime='%s')LIMIT 1" % (tableName,video_title, video_author, datetime_start, playNum, allPlayNum, tableName,tableName,video_author,datetime_start)
        # # print(sql)
        # # print(insertSql)
        # if index==0:
        #     cursor.execute(sql)
        # else:
        #     cursor.execute(insertSql)
        cursor.execute(sql)
        connect.commit()

