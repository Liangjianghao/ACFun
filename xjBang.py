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
tableName='savetable'
baseTime='2008-6-1'

# CREATE TABLE `savetable` (
#   `Id` int(11) NOT NULL AUTO_INCREMENT,
#   `video_title` varchar(255) DEFAULT NULL COMMENT '视频标题',
#   `video_author` varchar(255) DEFAULT NULL COMMENT '视频作者',
#   `video_uploadtime` date DEFAULT NULL COMMENT'更新时间',
#   `playNum` int(11) DEFAULT NULL COMMENT '播放',
#   `allPlayNum` int(11) DEFAULT NULL COMMENT '总播放',
#   PRIMARY KEY (`Id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='a站评论表';
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
    # sql = "SELECT *,sum(xjNum) as allnumber FROM %s WHERE video_uploadtime<='%s' GROUP BY video_author ORDER BY allnumber desc limit 20"%(baseTable,timeStr)
    sql="select * from %s  WHERE video_uploadtime<='%s' order by saveNum desc limit 20 "%(baseTable,timeStr)
    # newSql="SELECT * FROM (SELECT * FROM danceallzh  WHERE video_uploadtime<='%s' ORDER BY allPlayNum DESC LIMIT 15000) t GROUP BY video_author  ORDER BY allPlayNum DESC limit 20"%timeStr
    print(sql)
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchall()
    return data

datetime_start = parser.parse(baseTime)

nowTime = datetime.datetime.now()  # 现在

while datetime_start<nowTime:
    datetime_start = datetime_start + datetime.timedelta(days=2)
    print('处理时间段%s'%(datetime_start))
    videoArr=getinfor(datetime_start)
    print(len(videoArr))
    for index,video in enumerate(videoArr):
        video_title = video['video_title']
        # video_author = video['video_author']
        video_author = video['video_url'].split('v/')[1]
        # print(video_author)
        video_uploadtime = str(video['video_uploadtime'])[0:10]
        playNum = video['playNum']
        allPlayNum = video['saveNum']
        sql = "insert into %s(video_title,video_author,video_uploadtime,playNum,allPlayNum)values ('%s','%s', '%s','%s','%s')" % (tableName,video_title, video_author, datetime_start, playNum, allPlayNum)
        cursor.execute(sql)
        connect.commit()

    # break


