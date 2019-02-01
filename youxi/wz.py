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


baseTable='acatable'
tableName='wenzhangT'


# CREATE TABLE `wenzhangT` (
#   `Id` int(11) NOT NULL AUTO_INCREMENT,
#   `video_title` varchar(255) DEFAULT NULL COMMENT '视频标题',
#   `video_author` varchar(255) DEFAULT NULL COMMENT '视频作者',
#   `video_uploadtime` date DEFAULT NULL COMMENT'更新时间',
#   `playNum` int(11) DEFAULT NULL COMMENT '播放',
#   `allPlayNum` int(11) DEFAULT NULL COMMENT '总播放',
#   PRIMARY KEY (`Id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='a站文章结果表';


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
def getdace():
    sql = "SELECT *FROM acatable ORDER BY video_uploadtime"
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchall()
    return data
videoArr=getdace()
print(len(videoArr))
def analyVideo(index,video):
    print('正在处理第%s条数据:%s'%(str(index+1),video['video_title']))
    # sql='select *from actableAll where video_author="%s" ORDER BY allPlayNum DESC'%video['video_author']
    sql='SELECT *,SUM(playNum) AS allPlayNum FROM (SELECT * FROM wenzhangT ORDER BY allPlayNum DESC LIMIT 400000) t WHERE video_author="%s" '%video['video_author']
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchone()
    # print(data)
    video_title=video['video_title']
    video_author=video['video_author']
    video_uploadtime=str(video['video_uploadtime'])[0:10]
    xjNum=video['xjNum']
    if data['Id'] is None:
        allXjNum=video['playNum']
    else:
        allXjNum=data['allPlayNum']+video['playNum']
    sql="insert into wenzhangT(video_title,video_author,video_uploadtime,playNum,allPlayNum)values ('%s','%s','%s','%s', '%s')"%(video_title,video_author,video_uploadtime,xjNum,allXjNum)
    cursor.execute(sql)
    connect.commit()

for index,video in enumerate(videoArr):
    try:
        analyVideo(index,video)
    except Exception as e:
        continue


