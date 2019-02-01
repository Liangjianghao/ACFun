#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/8/17 14:23
# @Author : LiangJiangHao
# @Software: PyCharm
import os
import sys
import requests
import json
import time
import datetime
import pymysql

tableName='YY_yuanchuang'
# CREATE TABLE `YY_yuanchuang` (
#   `Id` int(11) NOT NULL AUTO_INCREMENT,
#   `video_title` varchar(255) DEFAULT NULL COMMENT '视频标题',
#   `video_url` varchar(255) DEFAULT NULL COMMENT '视频地址',
#   `video_author` varchar(255) DEFAULT NULL COMMENT '视频作者',
#   `video_uploadtime` datetime DEFAULT NULL COMMENT'视频上传时间',
#   `playNum` int(11) DEFAULT NULL COMMENT '播放',
#   `danmuNum` int(11) DEFAULT NULL COMMENT '弹幕数',
#   `comments` int(11) DEFAULT NULL COMMENT '评论数',
#   `saveNum` int(11) DEFAULT NULL COMMENT '收藏数',
#   `xjNum` int(11) DEFAULT NULL COMMENT '香蕉数',
#   PRIMARY KEY (`Id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='a站音乐原创表';

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

def insertChatContent(video_title,video_url,video_author,video_uploadtime, playNum, danmuNum, comments, saveNum, xjNum):
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
    sql = "INSERT INTO %s (video_title,video_url,video_author,video_uploadtime,playNum,danmuNum,comments,saveNum,xjNum) VALUES ('%s','%s', '%s','%s','%s','%s', '%s','%s','%s')" % (tableName,video_title,video_url,video_author, video_uploadtime, playNum, danmuNum, comments, saveNum, xjNum)
    print(sql)
    insertSql = "INSERT INTO %s (video_title,video_url,video_author,video_uploadtime,playNum,danmuNum,comments,saveNum,xjNum)SELECT '%s','%s', '%s','%s','%s','%s', '%s','%s','%s' FROM %s WHERE NOT EXISTS(SELECT video_url FROM %s WHERE video_url='%s')LIMIT 1" % (tableName,video_title,video_url,video_author, video_uploadtime, playNum, danmuNum, comments, saveNum, xjNum,tableName,tableName,video_url)

    cursor.execute(insertSql)
    connect.commit()
def getDetailInfo(url):
    baseArr=[]
    try:
        # print('正在解析第%s条视频数据：%s'%(str(index+1),url))
        userInfoUrl='http://webapi.aixifan.com/query/user?userId=13215999'
        id = url.split('/ac')[1]
        detailUrl = 'http://www.acfun.cn/content_view.aspx?contentId=%s' % id
        response = requests.get(detailUrl,headers=headers).content
        jsonData = json.loads(response)
        # print(jsonData)
        playNum = jsonData[0]
        danmuNum = jsonData[4]
        contenNum = jsonData[1]
        saveNum = jsonData[5]
        xjNum = jsonData[6]
        baseArr=[playNum,danmuNum,contenNum,saveNum,xjNum]
        # insertChatContent(id, playNum, danmuNum, contenNum, saveNum, xjNum)
    except  Exception as e:
        print('报错 %s'%e)
        # continue
    return baseArr

todayTime = datetime.datetime.now().strftime('%m-%d')
for x in range(1,850):
    try:
        print('正在抓取第%s页'%x)
        UA = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.13 Safari/537.36"
        headers = {"User-Agent": UA, 'X-Requested-With': 'XMLHttpRequest'}
        # url='http://www.acfun.cn/list/getlist?channelId=135&sort=0&pageSize=20&pageNo=%s'%x
        url='http://www.acfun.cn/list/getlist?channelId=136&sort=0&pageSize=20&pageNo=%s'%x
        response=requests.get(url,headers=headers).content
        requests.adapters.DEFAULT_RETRIES = 5
        jsonData=json.loads(response)
        videoArr=jsonData['data']['data']
        print(len(videoArr))
        if len(videoArr)<20:
            break
        time.sleep(2)

        for index,video in enumerate(videoArr):
            id=video['id']
            url='http://www.acfun.cn/v/ac%s'%id
            # print(url)
            uploadTime=video['contributeTimeFormat']
            userName=video['username']
            videoTitle=video['title']
            infoArr=getDetailInfo(url)
            print('正在处理第%s条数据：%s'%(str(index+1),videoTitle))
            # insertChatContent(videoTitle,url,userName,uploadTime,infoArr[0],infoArr[1],infoArr[2],infoArr[3],infoArr[4])
            video_title=videoTitle
            video_url=url
            video_author=userName
            video_uploadtime=uploadTime
            playNum=infoArr[0]
            danmuNum=infoArr[1]
            comments=infoArr[2]
            saveNum=infoArr[3]
            xjNum=infoArr[4]
            cursor = connect.cursor()
            sql = "INSERT INTO %s (video_title,video_url,video_author,video_uploadtime,playNum,danmuNum,comments,saveNum,xjNum) VALUES ('%s','%s', '%s','%s','%s','%s', '%s','%s','%s')" % (tableName, video_title, video_url, video_author, video_uploadtime, playNum, danmuNum, comments, saveNum,xjNum)
            # print(sql)
            insertSql = "INSERT INTO %s (video_title,video_url,video_author,video_uploadtime,playNum,danmuNum,comments,saveNum,xjNum)SELECT '%s','%s', '%s','%s','%s','%s', '%s','%s','%s' FROM %s WHERE NOT EXISTS(SELECT video_url FROM %s WHERE video_url='%s')LIMIT 1" % (tableName, video_title, video_url, video_author, video_uploadtime, playNum, danmuNum, comments, saveNum,xjNum, tableName, tableName, video_url)
            if index == 0:
                cursor.execute(sql)
            else:
                cursor.execute(insertSql)
            connect.commit()

    except Exception as e:
        print(e)


