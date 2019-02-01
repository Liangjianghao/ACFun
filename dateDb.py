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

# CREATE TABLE `dancetest` (
#   `Id` int(11) NOT NULL AUTO_INCREMENT,
#   `video_title` varchar(255) DEFAULT NULL COMMENT '视频标题',
#   `video_author` varchar(255) DEFAULT NULL COMMENT '视频作者',
#   `video_uploadtime` date DEFAULT NULL COMMENT'更新时间',
#   `playNum` int(11) DEFAULT NULL COMMENT '播放',
#   `allPlayNum` int(11) DEFAULT NULL COMMENT '总播放',
#   PRIMARY KEY (`Id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='a站测试汇总表';
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
def getdance(timeStr):
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
    sql = "SELECT * FROM danceAllZH WHERE video_uploadtime<='%s' ORDER BY video_uploadtime"%timeStr
    # print(sql)
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchall()
    return data

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
    sql = "SELECT *,sum(playNum) as allnumber FROM danceAllZH WHERE video_uploadtime<='%s' GROUP BY video_author ORDER BY allnumber desc limit 20"%timeStr
    newSql="SELECT * FROM (SELECT * FROM danceallzh  WHERE video_uploadtime<='%s' ORDER BY allPlayNum DESC LIMIT 15000) t GROUP BY video_author  ORDER BY allPlayNum DESC limit 20"%timeStr
    # print(sql)
    cursor.execute(newSql)
    connect.commit()
    data = cursor.fetchall()
    return data

baseTime='2015-1-1'
datetime_start = parser.parse(baseTime)

nowTime = datetime.datetime.now()  # 现在

f=open('author.txt','a+')
while datetime_start<nowTime:
    datetime_start = datetime_start + datetime.timedelta(days=1)
    print('处理时间段%s'%(datetime_start))
    videoArr=getfort(datetime_start)
    print(len(videoArr))
    for video in videoArr:
        video_title = video['video_title']
        video_author = video['video_author']
        video_uploadtime = str(video['video_uploadtime'])[0:10]
        playNum = video['playNum']
        allPlayNum = video['allPlayNum']
        sql = "insert into dancetest2(video_title,video_author,video_uploadtime,playNum,allPlayNum)values ('%s','%s', '%s','%s','%s')" % (video_title, video_author, datetime_start, playNum, allPlayNum)
        # print(sql)
        insertSql = "INSERT INTO dancetest2 (video_title,video_author,video_uploadtime,playNum,allPlayNum)SELECT '%s','%s','%s','%s','%s' FROM dancetest2 WHERE NOT EXISTS(SELECT video_author FROM dancetest2 WHERE video_author='%s' and video_uploadtime='%s')LIMIT 1" % (video_title, video_author, datetime_start, playNum, allPlayNum, video_author,datetime_start)
        # print(sql)
        cursor.execute(insertSql)
        connect.commit()

# time.sleep(1000)
# while datetime_start<nowTime:
#     datetime_start = datetime_start + datetime.timedelta(days=1)
#     print('处理时间段%s'%(datetime_start))
#     videoArr=getdance(datetime_start)
#     # print(len(videoArr))
#     for video in videoArr:
#         video_title = video['video_title']
#         video_author = video['video_author']
#         video_uploadtime = str(video['video_uploadtime'])[0:10]
#         playNum = video['playNum']
#         allPlayNum = video['allPlayNum']
#         sql = "insert into dancetest(video_title,video_author,video_uploadtime,playNum,allPlayNum)values ('%s','%s', '%s','%s','%s')" % (video_title, video_author, datetime_start, playNum, allPlayNum)
#         # print(sql)
#         insertSql = "INSERT INTO dancetest (video_title,video_author,video_uploadtime,playNum,allPlayNum)SELECT '%s','%s','%s','%s','%s' FROM dancetest WHERE NOT EXISTS(SELECT video_author FROM dancetest WHERE video_author='%s' and video_uploadtime='%s')LIMIT 1" % (video_title, video_author, datetime_start, playNum, allPlayNum, video_author,datetime_start)
#         # print(insertSql)
#         sql="REPLACE into dancetest (video_title,video_author,video_uploadtime,playNum,allPlayNum)  values ('%s','%s','%s','%s','%s')"%(video_title, video_author, datetime_start, playNum, allPlayNum)
#         # print(sql)
#         cursor.execute(sql)
#         connect.commit()


        # time.sleep(5)
        # def analyVideo(index,video):
#     print('正在处理第%s条数据:%s'%(str(index+1),video['video_title']))
#     sql='select *from danceAllZH where video_author="%s" ORDER BY allPlayNum DESC'%video['video_author']
#     cursor.execute(sql)
#     connect.commit()
#     data = cursor.fetchone()
#     # print(data)
#     video_title=video['video_title']
#     video_author=video['video_author']
#     video_uploadtime=str(video['video_uploadtime'])[0:10]
#     # print(video_uploadtime)
#     playNum=video['playNum']
#     if data is None:
#         # print('none')
#         allPlayNum=video['playNum']
#     else:
#         # print('有数据')
#         # print(data['playNum'])
#         allPlayNum=video['playNum']+data['allPlayNum']
#     sql="insert into danceAllZH(video_title,video_author,video_uploadtime,playNum,allPlayNum)values ('%s','%s', '%s','%s','%s')"%(video_title,video_author,video_uploadtime,playNum,allPlayNum)
#     # print(sql)
#     cursor.execute(sql)
#     connect.commit()
#
# for index,video in enumerate(videoArr):
#     analyVideo(index,video)
