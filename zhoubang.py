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
tableName='acyb_8'
baseTime='2018-8-1'
endT='2018-9-1'
datetime_start = parser.parse(baseTime)
# endTime = datetime_start + datetime.timedelta(days=7)
endTime=parser.parse(endT)
# CREATE TABLE `acyb_8` (
#   `Id` int(11) NOT NULL AUTO_INCREMENT,
#   `video_title` varchar(255) DEFAULT NULL COMMENT '视频标题',
#   `video_author` varchar(255) DEFAULT NULL COMMENT '视频作者',
#   `video_uploadtime` date DEFAULT NULL COMMENT'更新时间',
#   `playNum` int(11) DEFAULT NULL COMMENT '播放',
#   `allPlayNum` int(11) DEFAULT NULL COMMENT '总播放',
#   PRIMARY KEY (`Id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='a站八月月榜总表';
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
    sql = "SELECT *,playNum/10+xjNum*20+saveNum*10+comments*10+danmuNum*5 AS total FROM %s WHERE video_uploadtime>'%s' AND video_uploadtime<'%s'  ORDER BY total DESC limit 20"%(baseTable,baseTime,timeStr)
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchall()
    return data



while datetime_start<endTime:
    videoArr=getinfor(datetime_start)
    print(len(videoArr))
    datetime_start = datetime_start + datetime.timedelta(days=1)
    print('处理时间段%s----%s'%(baseTime,datetime_start))
    for index,video in enumerate(videoArr):
        video_title = video['video_title']
        # video_author = video['video_author']
        video_author = video['video_url'].split('v/')[1]

        video_uploadtime = str(video['video_uploadtime'])[0:10]
        playNum = video['playNum']
        allPlayNum = video['total']
        sql = "INSERT into %s(video_title,video_author,video_uploadtime,playNum,allPlayNum)values ('%s','%s', '%s','%s','%s')" % (tableName,video_title, video_author, datetime_start, playNum, allPlayNum)
        cursor.execute(sql)
        connect.commit()

