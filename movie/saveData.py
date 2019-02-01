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
    # sql = "INSERT INTO dancezh (video_title,video_url,video_author,video_uploadtime,playNum,danmuNum,comments,saveNum,xjNum) VALUES ('%s','%s', '%s','%s','%s','%s', '%s','%s','%s')" % (video_title,video_url,video_author, video_uploadtime, playNum, danmuNum, comments, saveNum, xjNum)
    # print(sql)
    insertSql = "INSERT INTO dancezh (video_title,video_url,video_author,video_uploadtime,playNum,danmuNum,comments,saveNum,xjNum)SELECT '%s','%s', '%s','%s','%s','%s', '%s','%s','%s' FROM dancezh WHERE NOT EXISTS(SELECT video_url FROM dancezh WHERE video_url='%s')LIMIT 1" % (video_title,video_url,video_author, video_uploadtime, playNum, danmuNum, comments, saveNum, xjNum,video_url)

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
f=open('movie-%s.txt'%todayTime,'a+')
for x in range(1,800):
    try:
        print('正在抓取第%s页'%x)
        UA = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.13 Safari/537.36"
        headers = {"User-Agent": UA, 'X-Requested-With': 'XMLHttpRequest'}
        url='http://www.acfun.cn/list/getlist?channelId=135&sort=0&pageSize=20&pageNo=%s'%x
        response=requests.get(url,headers=headers).content
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
    except Exception as e:
        print(e)

