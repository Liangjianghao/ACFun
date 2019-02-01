#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/12/30 17:07
# @Author : LiangJiangHao
# @Software: PyCharm

import os
import sys
import requests
import pymysql
import urllib
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import time

# CREATE TABLE `AC_fence` (
#   `Id` INT(11) NOT NULL AUTO_INCREMENT,
#   `userid` INT(11) NOT NULL COMMENT '用户id',
#   `userImg` VARCHAR(255) DEFAULT NULL COMMENT '用户头像',
#   `user_name` VARCHAR(255) DEFAULT NULL COMMENT'用户名',
#   `followed` INT(11) DEFAULT NULL COMMENT '粉丝数',
#   `video_uploadtime` date DEFAULT NULL COMMENT '上传时间',
#   PRIMARY KEY (`Id`)
# ) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COMMENT='a站粉丝表';

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

def insertChatContent(userid,userImg,user_name,followed,video_uploadtime):
    # 连接数据库
    sql="insert into AC_fence (userid,userImg,user_name,followed,video_uploadtime)  values ('%s','%s', '%s','%s','%s')"%(userid,userImg,user_name,followed,video_uploadtime)
    cursor.execute(sql)
    connect.commit()
def selectData():
    # 连接数据库
    # sql='SELECT *FROM actable order by video_uploadtime limit 10'
    # sql='SELECT *FROM actable order by video_uploadtime'
    sql='SELECT *FROM (SELECT *FROM actable ORDER BY video_uploadtime LIMIT 1000000)t GROUP BY video_author'
    cursor.execute(sql)
    data=cursor.fetchall()
    return data

def getDetailByUserid(videoId,video_uploadtime):
    # print(videoId)
    # videoId='609656'
    # url='https://apipc.app.acfun.cn/v2/user/album?app_version=5.11.1&market=appstore&origin=ios&pageNo=1&pageSize=20&resolution=750x1334&sort=0&status=2&sys_name=ios&sys_version=12.0&userId=%s'%userId
    # header_dict = {'deviceType': '0'}
    url='https://apipc.app.acfun.cn/v2/videos/%s'%videoId
    header_dict = {'deviceType': '0'}
    response = requests.get(url, headers=header_dict, verify=False).content
    result = json.loads(response)
    inforList=result['vdata']['owner']
    # print(inforList)
    if len(inforList)==0:
        return
    else:
        # print(inforList[0])
        userImg=inforList['avatar']
        userId=inforList['id']
        userName=inforList['name']
        fenceNum=inforList['followed']

        # print(userImg)
        if '\\' in userName:
            userName = userName.replace("\\", "\\\\")
        if "'" in userName:
            userName = userName.replace("'", "\\'")
        if '"' in userName:
            userName = userName.replace('"', '\\"')
        if 'jpg' not in userImg:
            userImg = ''
        if '万' in fenceNum:
            fenceNum=int(float(fenceNum.split('万')[0])*10000)
        insertChatContent(userId,userImg,userName,fenceNum,video_uploadtime)

    # url = "https://apipc.app.acfun.cn/v2/user/album"
    # querystring = {"app_version": "5.11.1", "market": "appstore", "origin": "ios", "pageNo": "1", "pageSize": "20",
    #                "resolution": "750x1334", "sort": "0", "status": "2", "sys_name": "ios", "sys_version": "12.0",
    #                "userId": "1155262"}
    # headers = {
    #     'deviceType': "0",
    # }
    # response = requests.request("GET", url, headers=headers, params=querystring,verify=False)
    # print(response.text)


videoArr=selectData()
print(len(videoArr))

for index,video in enumerate(videoArr):
    # time.sleep(1)
    title = video['video_title']
    uploadTime=str(video['video_uploadtime'])[0:10]
    # print(uploadTime)
    print('正在采集第%s条视频数据:%s'%(index+1,title))
    try:
        videoId=video['video_url'].split('/ac')[1]
        getDetailByUserid(videoId,uploadTime)
    except Exception as e:
        print(e)
        continue
    # break
