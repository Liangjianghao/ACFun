#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/3 12:06
# @Author : LiangJiangHao
# @Software: PyCharm
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
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
baseTable='ac2018'
tableName='ac2018Result'
baseTime='2018-1-1'
import json

# CREATE TABLE `ac2018Result` (
#   `Id` int(11) NOT NULL AUTO_INCREMENT,
#   `video_title` varchar(255) DEFAULT NULL COMMENT '视频标题',
#   `video_url` varchar(255) DEFAULT NULL COMMENT '视频地址',
#   `video_cover` varchar(255) DEFAULT NULL COMMENT '封面地址',
#   `video_author` varchar(255) DEFAULT NULL COMMENT '视频作者',
#   `video_uploadtime` datetime DEFAULT NULL COMMENT'视频上传时间',
#   `playNum` int(11) DEFAULT NULL COMMENT '播放',
#   `danmuNum` int(11) DEFAULT NULL COMMENT '弹幕数',
#   `comments` int(11) DEFAULT NULL COMMENT '评论数',
#   `saveNum` int(11) DEFAULT NULL COMMENT '收藏数',
#   `xjNum` int(11) DEFAULT NULL COMMENT '香蕉数',
#   `video_type` varchar(255) DEFAULT NULL COMMENT '视频类型',
#   `danmu_id` varchar(255) DEFAULT NULL COMMENT '弹幕id',
#  `score` int(11) DEFAULT NULL COMMENT '评分',
#     PRIMARY KEY (`Id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='a站2018排序表';

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

    sql='SELECT * FROM %s WHERE video_uploadtime<"%s" ORDER BY score DESC LIMIT 20'%(baseTable,timeStr)
    print(sql)
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchall()
    return data

datetime_start = parser.parse(baseTime)
nowTime = datetime.datetime.now()  # 现在


while datetime_start<nowTime:
    datetime_start = datetime_start + datetime.timedelta(days=1)
    print('处理时间段%s'%(datetime_start))
    videoArr=getinfor(datetime_start)
    print(len(videoArr))
    for index,video in enumerate(videoArr):
        try:
            title = video['video_title']
            video_cover = video['video_cover']
            videoUrl = video['video_url']
            video_author = video['video_author']
            # video_uploadtime = str(video['video_uploadtime'])[0:10]
            playNum = video['playNum']
            danmuNum = video['danmuNum']
            comments = video['comments']
            saveNum = video['saveNum']
            xjNum = video['xjNum']
            video_type = video['video_type']
            danmu_id = video['danmu_id']
            score = video['score']

            insertStr = "insert into ac2018Result (video_title,video_cover,video_url,video_author,video_uploadtime,playNum,danmuNum,comments,saveNum,xjNum,video_type,danmu_id,score)  values ('%s','%s', '%s','%s','%s','%s','%s','%s', '%s','%s','%s','%s','%s')" \
                        %(title,video_cover,videoUrl,video_author,datetime_start,playNum,danmuNum,comments,saveNum,xjNum,video_type,danmu_id,score)
            # print(insertStr)
            cursor.execute(insertStr)
            connect.commit()
        except Exception as e:
            print(e)
            continue


