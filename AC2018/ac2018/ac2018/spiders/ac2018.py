#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/2 11:55
# @Author : LiangJiangHao
# @Software: PyCharm

import scrapy
import os
import requests
import json
from scrapy.http import Request
import pymysql
from scrapy.spider import Spider
from ac2018.items import Ac2018Item
import time
import random

with open('F:\ACFun\AC2018\\acType.json',encoding='utf-8') as f:
    typeDic=json.load(f)

user_agent_list = [ \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

class Myspider(scrapy.Spider):
    name='ac2018'
    allowed_domains=['https://apipc.app.acfun.cn']
    base_url='https://apipc.app.acfun.cn/v2/user/content/profile?app_version=5.10.2&market=appstore&origin=ios&resolution=750x1334&sys_name=ios&sys_version=12.0&userId=1'

    def start_requests(self):
        # for x in range(250000, 14500000):

        for x in range(4820000, 48350000):
        # for x in range(4150000, 4151000):
        #     time.sleep(2)
            ua = random.choice(user_agent_list)
            self.headers = {
                'User-Agent': ua,
                'deviceType':0
            }
            url = "https://apipc.app.acfun.cn/v2/videos/%s" % x
            yield Request(url,headers=self.headers,callback=self.parse,meta={'url':url,'videoid':x})
    def parse(self,response):
        # print(response.text)
        try:
            result = json.loads(response.text)
            if result['errorid']>0:
                return
            videoUrl=response.meta['url']
            videoid=response.meta['videoid']

            # danmu_id =str(result['vdata']['channelId']) + '-' + str(result['vdata']['parentChannelId'])
            danmu_id = result['vdata']['videos'][0]['videoId']
            type_id = str(result['vdata']['parentChannelId']) + '-' + str(result['vdata']['channelId'])
            title = result['vdata']['title']
            video_cover = result['vdata']['cover']
            video_author = result['vdata']['owner']['name']
            uploadtime = str(result['vdata']['releaseDate'])[:-3]
            video_uploadtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(uploadtime)))

            playNum = result['vdata']['visit']['views']
            danmuNum = result['vdata']['visit']['danmakuSize']
            comments = result['vdata']['visit']['comments']
            saveNum = result['vdata']['visit']['stows']
            xjNum = result['vdata']['visit']['goldBanana']
            score = playNum / 10 + xjNum * 20 + saveNum * 10 + comments * 10 + danmuNum * 5
            # video_type = typeDic[type_id]
            video_type = '类型'
            title=self.checkStr(title)
            video_author=self.checkStr(video_author)

            iterm=Ac2018Item()
            print('正在抓取第%s条数据:%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s'%(videoid,title,video_cover,videoUrl,video_author,video_uploadtime,playNum,danmuNum,comments,saveNum,xjNum,video_type,danmu_id,score))
            # insertChatContent(userid,userImg,userName,fenceNum,bananaGold)
            # print(userName)
            iterm['title']=title
            iterm['video_cover']=video_cover
            iterm['videoUrl']=videoUrl
            iterm['video_author']=video_author
            iterm['video_uploadtime']=video_uploadtime
            iterm['playNum'] = playNum
            iterm['danmuNum'] = danmuNum
            iterm['comments'] = comments
            iterm['saveNum'] = saveNum
            iterm['xjNum'] = xjNum
            iterm['video_type'] = video_type
            iterm['danmu_id'] = danmu_id
            iterm['score'] = score


            yield iterm
        except Exception as e:
            print('解析数据parse:%s'%e)

    def checkStr(self,theStr):
        if '\\' in theStr:
            theStr = theStr.replace("\\", "\\\\")
        if "'" in theStr:
            theStr = theStr.replace("'", "\\'")
        if '"' in theStr:
            theStr = theStr.replace('"', '\\"')
        return theStr
