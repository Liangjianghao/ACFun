#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/10/15 8:14
# @Author : LiangJiangHao
# @Software: PyCharm
import requests
from lxml import html


UA = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.13 Safari/537.36"
headers = {"User-Agent": UA}

url = 'https://movie.douban.com/subject/27110296/'
print(url)
response = requests.get(url, headers=headers, verify=False).content
# print(response)
# f.write(response)
# f.close()
selector = html.fromstring(response)
typeSelect = selector.xpath('//*[@id="info"]/span[contains(text(),"类型")]/following-sibling::*/text()')[0]
# print(type(typeSelect))

print(typeSelect)
movietype = typeSelect[0]
# productInfo = selector.xpath('//*[@id="info"]/span[contains(@text(),"-")]')
productInfo = selector.xpath('//*[@id="info"]/span[contains(text(),"首播")]/following-sibling::*/text()')
if len(productInfo)==0:
    productInfo = selector.xpath('//*[@id="info"]/span[contains(text(),"上映日期")]/following-sibling::*/text()')

if len(productInfo[0])==4:
    uptime='%s-1-1'%productInfo[0]
else:
    uptime=productInfo[0]
print(uptime)
# print(productInfo)
# for info in productInfo:
#     print(info)
# if '(' in productInfo[0]:
#     uptime = productInfo[0].split('(')[0]
# else:
#     uptime = productInfo[0]