# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DoubanItem(scrapy.Item):
    title = scrapy.Field()
    id = scrapy.Field()
    rate = scrapy.Field()
    url = scrapy.Field()
    cover = scrapy.Field()
    uploadTime=scrapy.Field()
