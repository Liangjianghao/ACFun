#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/8/29 12:46
# @Author : LiangJiangHao
# @Software: PyCharm
import pymysql
import os
import sys
import time
# CREATE TABLE `actableAll2` (
#   `Id` int(11) NOT NULL AUTO_INCREMENT,
#   `video_title` varchar(255) DEFAULT NULL COMMENT '视频标题',
#   `video_author` varchar(255) DEFAULT NULL COMMENT '视频作者',
#   `video_uploadtime` date DEFAULT NULL COMMENT'更新时间',
#   `xjNum` int(11) DEFAULT NULL COMMENT '香蕉',
#   `allXjNum` int(11) DEFAULT NULL COMMENT '总香蕉',
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
    # connect = pymysql.Connect(
    #     host='192.168.2.101',
    #     port=3306,
    #     user='root',
    #     passwd='123456',
    #     db='acfun',
    #     charset='utf8mb4',
    #     cursorclass = pymysql.cursors.DictCursor
    #
    # )
    # cursor = connect.cursor()
    sql = "SELECT *FROM actable ORDER BY video_uploadtime"
    # sql='SELECT *FROM actable WHERE video_author="熊猫" ORDER BY video_uploadtime'
    # print(sql)
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchall()
    return data
videoArr=getdace()
print(len(videoArr))
def analyVideo(index,video):
    print('正在处理第%s条数据:%s'%(str(index+1),video['video_title']))
    # sql='select *from actableAll where video_author="%s" ORDER BY allPlayNum DESC'%video['video_author']
    sql='SELECT Id,video_author,video_uploadtime,xjNum,SUM(xjNum) AS allXjNum FROM (SELECT * FROM actableall2 ORDER BY allXjNum DESC LIMIT 800000) t WHERE video_author="%s" '%video['video_author']
    # print(sql)
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchone()
    # print(data)
    # video_title=video['video_title']
    video_title='123'
    video_author=video['video_author']
    video_uploadtime=str(video['video_uploadtime'])[0:10]
    xjNum=video['xjNum']
    if data['Id'] is None:
        allXjNum=video['xjNum']
    else:
        allXjNum=data['allXjNum']+video['xjNum']
    sql="insert into actableAll2(video_title,video_author,video_uploadtime,xjNum,allXjNum)values ('%s','%s','%s','%s', '%s')"%(video_title,video_author,video_uploadtime,xjNum,allXjNum)

    # print(sql)
    cursor.execute(sql)
    connect.commit()

for index,video in enumerate(videoArr):
    analyVideo(index,video)


