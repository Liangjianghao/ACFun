#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/2 11:28
# @Author : LiangJiangHao
# @Software: PyCharm

import os
import requests
import json
import pymysql
import time
import datetime
# CREATE TABLE `ac2018` (
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
#  `score` varchar(255) DEFAULT NULL COMMENT '评分',
#     PRIMARY KEY (`Id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='a站2018表';
with open('acType.json',encoding='utf-8') as f:
    typeDic=json.load(f)

def insertChatContent(video_title,video_cover,video_url,video_author,video_uploadtime, playNum, danmuNum, comments, saveNum, xjNum,video_type,danmu_id,score):
    # 连接数据库
    connect = pymysql.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='acfun',
        charset='utf8mb4'
    )
    # 获取游标
    cursor = connect.cursor()
    sql="REPLACE into ac2018 (video_title,video_cover,video_url,video_author,video_uploadtime,playNum,danmuNum,comments,saveNum,xjNum,video_type,danmu_id,score)  values ('%s','%s', '%s','%s','%s','%s', '%s','%s','%s','%s','%s','%s','%s')"%(video_title,video_cover,video_url,video_author, video_uploadtime, playNum, danmuNum, comments, saveNum, xjNum,video_type,danmu_id,score)
    # print(sql)
    cursor.execute(sql)
    connect.commit()

def analyVideo(videoUrl):
    # videoUrl='http://www.acfun.cn/v/ac4418710'
    idStr=videoUrl.split('/ac')[1]
    header_dict = {'deviceType': '0'}
    url = "https://apipc.app.acfun.cn/v2/videos/%s" % idStr
    print(url)
    res = requests.get(url, headers=header_dict,verify=False).content
    result = json.loads(res)
    # danmu_id =str(result['vdata']['channelId']) + '-' + str(result['vdata']['parentChannelId'])
    danmu_id= result['vdata']['videos'][0]['videoId']

    type_id= str(result['vdata']['parentChannelId']) + '-' + str(result['vdata']['channelId'])
    title=result['vdata']['title']
    video_cover=result['vdata']['cover']

    video_author=result['vdata']['owner']['name']
    uploadtime=str(result['vdata']['releaseDate'])[:-3]
    video_uploadtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(uploadtime)))

    playNum=result['vdata']['visit']['views']
    danmuNum=result['vdata']['visit']['danmakuSize']
    comments=result['vdata']['visit']['comments']
    saveNum=result['vdata']['visit']['stows']
    xjNum=result['vdata']['visit']['goldBanana']
    score=playNum/10+xjNum*20+saveNum*10+comments*10+danmuNum*5

    video_type=typeDic[type_id]
    insertChatContent(title,video_cover,videoUrl,video_author,video_uploadtime,playNum,danmuNum,comments,saveNum,xjNum,video_type,danmu_id,score)

for x in range(4000000,4001000):
    print('正在采集第%s个视频'%str(x))
    url='http://www.acfun.cn/v/ac%s'%x
    try:
        analyVideo(url)
    except Exception as e:
        print('报错：%s'%e)
        continue