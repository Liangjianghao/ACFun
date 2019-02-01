#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/8/29 12:46
# @Author : LiangJiangHao
# @Software: PyCharm
import pymysql
import os
import sys
import time
# CREATE TABLE `actableAll` (
#   `Id` int(11) NOT NULL AUTO_INCREMENT,
#   `video_title` varchar(255) DEFAULT NULL COMMENT '视频标题',
#   `video_author` varchar(255) DEFAULT NULL COMMENT '视频作者',
#   `video_uploadtime` date DEFAULT NULL COMMENT'更新时间',
#   `playNum` int(11) DEFAULT NULL COMMENT '播放',
#   `allPlayNum` int(11) DEFAULT NULL COMMENT '总播放',
#   `danmuNum` int(11) DEFAULT NULL COMMENT '播放',
#   `allDmNum` int(11) DEFAULT NULL COMMENT '总播放',
#   `comments` int(11) DEFAULT NULL COMMENT '播放',
#   `allCmNum` int(11) DEFAULT NULL COMMENT '总播放',
#   `saveNum` int(11) DEFAULT NULL COMMENT '播放',
#   `allSaveNum` int(11) DEFAULT NULL COMMENT '总播放',
#   `xjNum` int(11) DEFAULT NULL COMMENT '播放',
#   `allXjNum` int(11) DEFAULT NULL COMMENT '总播放',
#   PRIMARY KEY (`Id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='a站总总表';
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
    sql = "SELECT *FROM actable ORDER BY video_uploadtime"
    sql='SELECT *FROM actable WHERE video_author="熊猫" ORDER BY video_uploadtime'

    print(sql)
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchall()
    return data
videoArr=getdace()
print(len(videoArr))
def analyVideo(index,video):
    print('正在处理第%s条数据:%s'%(str(index+1),video['video_title']))
    # sql='select *from actableAll where video_author="%s" ORDER BY allPlayNum DESC'%video['video_author']
    sql='SELECT *,SUM(playNum) AS allPlayNum,SUM(danmuNum) AS allDmNum,SUM(comments) AS allCmNum,SUM(saveNum) AS allSaveNum,SUM(xjNum) AS allXjNum FROM actableAll WHERE video_author="%s" ORDER BY video_uploadtime DESC'%video['video_author']
    # print(sql)
    sql='SELECT *,SUM(playNum) AS allPlayNum,SUM(danmuNum) AS allDmNum,SUM(comments) AS allCmNum,SUM(saveNum) AS allSaveNum,SUM(xjNum) AS allXjNum FROM (SELECT * FROM actableall ORDER BY video_uploadtime DESC LIMIT 800000) t WHERE video_author="%s" '%video['video_author']
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchone()
    # print(data['Id'])
    video_title=video['video_title']
    video_author=video['video_author']
    video_uploadtime=str(video['video_uploadtime'])[0:10]
    # print(video_uploadtime)
    playNum=video['playNum']
    danmuNum=video['danmuNum']
    comments=video['comments']
    saveNum=video['saveNum']
    xjNum=video['xjNum']

    if data['Id'] is None:
        allPlayNum=video['playNum']
        allDmNum=video['danmuNum']
        allCmNum=video['comments']
        allSaveNum=video['saveNum']
        allXjNum=video['xjNum']
    else:
        # print(2)
        allPlayNum=data['allPlayNum']+video['playNum']
        allDmNum=data['allDmNum']+video['danmuNum']
        allCmNum=data['allCmNum']+video['comments']
        allSaveNum=data['allSaveNum']+video['saveNum']
        allXjNum=data['allXjNum']+video['xjNum']
        # print(data['allXjNum'])
        # print(video['xjNum'])
    # if index==3:
    #     time.sleep(100)

    sql="insert into actableAll(video_title,video_author,video_uploadtime,playNum,allPlayNum,danmuNum,allDmNum,comments,allCmNum,saveNum,allSaveNum,xjNum,allXjNum)values ('%s','%s', '%s','%s','%s','%s','%s', '%s','%s','%s','%s','%s', '%s')"%(video_title,video_author,video_uploadtime,playNum,allPlayNum,danmuNum,allDmNum,comments,allCmNum,saveNum,allSaveNum,xjNum,allXjNum)

    print(sql)
    cursor.execute(sql)
    connect.commit()

for index,video in enumerate(videoArr):
    analyVideo(index,video)
# ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '123456';
# ALTER USER 'root'@'localhost' IDENTIFIED BY '!12345
