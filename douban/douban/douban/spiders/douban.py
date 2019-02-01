#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/1 0:24
# @Author : LiangJiangHao
# @Software: PyCharm

import scrapy
import os
import requests
import json
from scrapy.http import Request
import pymysql
from scrapy.spider import Spider
import time
import random
from douban.items import DoubanItem
from lxml import html


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
    name='douban'
    allowed_domains=['douban.com/']
    base_url='https://www.douban.com/'

    def start_requests(self):

        for x in range(1, 2):
            ua = random.choice(user_agent_list)
            self.headers = {
                'User-Agent': ua,
                'host': 'movie.douban.com',
                'referer':'https://movie.douban.com/tag/',
                'Upgrade-Insecure-Requests': '1',
                # 'cookie':
                # '_ga=GA1.2.1839800985.1501204775; bid=eR6knobXpJo; __guid=223695111.3490694355635478500.1533725893583.0178; douban-fav-remind=1; _vwo_uuid_v2=621DCA8C746F4B3DF093B54415B9F329|375b78efe9b94198d4b0c975d446a577; ll="108296"; viewed="1007305"; gr_user_id=70e4527b-c689-4654-9f35-c1e456582152; _gid=GA1.2.436967006.1546277888; ps=y; ue="1084933098@qq.com"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.12366; douban-profile-remind=1; __utmc=30149280; __utmz=30149280.1546411627.17.11.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmc=223695111; __utma=30149280.1839800985.1501204775.1546411627.1546419449.18; __utmt=1; dbcl2="123668881:OUBPoGEjFKw"; ck=wxgX; __utmb=30149280.9.10.1546419449; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1546419804%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=223695111.1839800985.1501204775.1546411630.1546419804.12; __utmb=223695111.0.10.1546419804; __utmz=223695111.1546419804.12.9.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; monitor_count=16; _pk_id.100001.4cf6=4a988360b0fa882d.1538568199.12.1546419808.1546414055.'
            }
            url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=&start=%s&genres=喜剧&year_range=2018,2018' % int(x * 20)
            # url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=&start=0&genres=动画&year_range=2018,2018'% int(x * 20)
            # response = requests.get(url, headers=self.headers, verify=False).content
            # print(response)
            time.sleep(2)
            yield Request(url, headers=self.headers,callback=self.parse)
            # yield Request(url,callback=self.parse)

    def parse(self,response):
        print(response.text)
        try:
            result = json.loads(response.text)
            # print(result)
            videoArr=result['data']
            # print(len(videoArr))
            if len(videoArr)==0:
                print('******************************************')
                return
            for video in videoArr:
                iterm=DoubanItem()
                title = video['title']
                id = video['id']
                rate = video['rate']
                url = video['url']
                cover = video['cover']
                uploadTime = self.getUpTime(url)

                sqlStr='%s,%s,%s,%s,%s,%s'%(title,id,rate,url,cover,uploadTime)
                print(sqlStr)
                if '\\' in title:
                    title = title.replace("\\", "\\\\")
                if "'" in title:
                    title=title.replace("'","\\'")
                if '"' in title:
                    title = title.replace('"', '\\"')
                if rate=='':
                    rate=0
                iterm['title']=title
                iterm['id']=id
                iterm['rate']=rate
                iterm['url']=url
                iterm['cover']=cover
                iterm['uploadTime']=uploadTime
                yield iterm
        except Exception as e:
            print('parseException:%s'%e)
    def getUpTime(self,url):
        response = requests.get(url, verify=False).content
        selector = html.fromstring(response)
        productInfo = selector.xpath('//*[@id="info"]/span[contains(text(),"首播")]/following-sibling::*/text()')
        if len(productInfo) == 0:
            productInfo = selector.xpath('//*[@id="info"]/span[contains(text(),"上映日期")]/following-sibling::*/text()')
        if '(' in productInfo[0]:
            uptime = productInfo[0].split('(')[0]
        else:
            uptime = productInfo[0]
        if len(uptime) == 4:
            uptime = '%s-1-1' % uptime
        print(uptime)
        return  uptime

