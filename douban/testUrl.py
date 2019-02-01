#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/1 13:11
# @Author : LiangJiangHao
# @Software: PyCharm

import random
from lxml import html
import requests
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
class testUrl(object):
    def __init__(self, value=0):
        self.thing = value
        self.test()

    def test(self):
        print(self.thing)
        ua = random.choice(user_agent_list)
        self.headers = {
            'User-Agent': ua,
            'host': 'movie.douban.com',
            'Upgrade-Insecure-Requests':'1',
            'cookie': '_ga=GA1.2.1839800985.1501204775; bid=eR6knobXpJo; __guid=223695111.3490694355635478500.1533725893583.0178; douban-fav-remind=1; _vwo_uuid_v2=621DCA8C746F4B3DF093B54415B9F329|375b78efe9b94198d4b0c975d446a577; ll="108296"; viewed="1007305"; gr_user_id=70e4527b-c689-4654-9f35-c1e456582152; __utmc=30149280; _gid=GA1.2.436967006.1546277888; ps=y; ue="1084933098@qq.com"; dbcl2="123668881:twRP1/FcpgY"; ck=6h0X; push_noty_num=0; push_doumail_num=0; __utmv=30149280.12366; douban-profile-remind=1; __utmc=223695111; monitor_count=13; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1546314814%2C%22http%3A%2F%2Fpython.jobbole.com%2F88325%2F%22%5D; _pk_id.100001.4cf6=4a988360b0fa882d.1538568199.10.1546314814.1546283010.; _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=30149280.1839800985.1501204775.1546283003.1546314814.15; __utmb=30149280.0.10.1546314814; __utmz=30149280.1546314814.15.9.utmcsr=python.jobbole.com|utmccn=(referral)|utmcmd=referral|utmcct=/88325/; __utma=223695111.1839800985.1501204775.1546283003.1546314814.10; __utmb=223695111.0.10.1546314814; __utmz=223695111.1546314814.10.7.utmcsr=python.jobbole.com|utmccn=(referral)|utmcmd=referral|utmcct=/88325/',
        }
        url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=&start=%s&genres=喜剧&countries=中国大陆&year_range=2018,2018' % int(1 * 20)
        response=requests.get(url,headers=self.headers,verify=False).content
        print(response)

test=testUrl(1)