#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/8/29 12:46
# @Author : LiangJiangHao
# @Software: PyCharm
import pymysql
import os
import sys
import time
# CREATE TABLE `danceAllZH` (
#   `Id` int(11) NOT NULL AUTO_INCREMENT,
#   `video_title` varchar(255) DEFAULT NULL COMMENT '视频标题',
#   `video_author` varchar(255) DEFAULT NULL COMMENT '视频作者',
#   `video_uploadtime` date DEFAULT NULL COMMENT'更新时间',
#   `playNum` int(11) DEFAULT NULL COMMENT '播放',
#   `allPlayNum` int(11) DEFAULT NULL COMMENT '总播放',
#   PRIMARY KEY (`Id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='a站舞蹈汇总表';
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
    sql = "SELECT *FROM dancezh ORDER BY video_uploadtime"
    print(sql)
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchall()
    return data
videoArr=getdace()
print(len(videoArr))
def analyVideo(index,video):
    print('正在处理第%s条数据:%s'%(str(index+1),video['video_title']))
    sql='select *from danceAllZH where video_author="%s" ORDER BY allPlayNum DESC'%video['video_author']
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchone()
    # print(data)
    video_title=video['video_title']
    video_author=video['video_author']
    video_uploadtime=str(video['video_uploadtime'])[0:10]
    # print(video_uploadtime)
    playNum=video['playNum']
    if data is None:
        # print('none')
        allPlayNum=video['playNum']
    else:
        # print('有数据')
        # print(data['playNum'])
        allPlayNum=video['playNum']+data['allPlayNum']
    sql="insert into danceAllZH(video_title,video_author,video_uploadtime,playNum,allPlayNum)values ('%s','%s', '%s','%s','%s')"%(video_title,video_author,video_uploadtime,playNum,allPlayNum)

    # print(sql)
    cursor.execute(sql)
    connect.commit()

for index,video in enumerate(videoArr):
    analyVideo(index,video)
