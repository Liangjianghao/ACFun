#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/2 21:31
# @Author : LiangJiangHao
# @Software: PyCharm
import requests
import json
import pymysql
import time

# 连接数据库
connect = pymysql.Connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='123456',
    db='acfun',
    charset='utf8mb4',
    cursorclass = pymysql.cursors.DictCursor

)
# 获取游标
cursor = connect.cursor()
def insertChatContent(video_title,video_id,video_uploadtime,score):

    sql="replace into ac2018new(video_title,video_id,video_uploadtime,score)  values ('%s','%s','%s','%s')"%(video_title,video_id,video_uploadtime,score)
    print(sql)
    cursor.execute(sql)
    connect.commit()

def seletData():
    sql='select * from ac2018Result'
    cursor.execute(sql)
    data=cursor.fetchall()
    return data

videoArr=seletData()
for index,video in enumerate(videoArr):
    print(index+1)
    video_id='ac%s'%(video['video_url'].split('videos/')[1])
    insertChatContent(video['video_title'],video_id,video['video_uploadtime'],video['score'])
# CREATE TABLE `ac2018new2` (
#   `Id` int(11) NOT NULL AUTO_INCREMENT,
#   `video_title` varchar(255) DEFAULT NULL COMMENT '视频标题',
#   `video_id` varchar(255) DEFAULT NULL COMMENT '视频id',
#   `video_uploadtime` date DEFAULT NULL COMMENT'视频上传时间',
#  `score` varchar(255) DEFAULT NULL COMMENT '评分',
#     PRIMARY KEY (`Id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='a站2018表';