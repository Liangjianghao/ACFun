# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import time
# CREATE TABLE `DB_xiju` (
# #   `Id` INT(11) NOT NULL AUTO_INCREMENT,
# #   `title` VARCHAR(255) NOT NULL COMMENT '电影名',
# #   `movie_id` VARCHAR(255) DEFAULT NULL COMMENT '电影id',
# #   `rate` FLOAT(11) DEFAULT NULL COMMENT'评分',
# #   `url` VARCHAR(255) DEFAULT NULL COMMENT '网址',
# #   `cover` VARCHAR(255) DEFAULT NULL COMMENT '封面',
# #   `uploadTime` date DEFAULT NULL COMMENT '上映时间',
# #   PRIMARY KEY (`Id`)
# # ) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COMMENT='豆瓣喜剧';

# CREATE TABLE `DB_dongman` (
#   `Id` INT(11) NOT NULL AUTO_INCREMENT,
#   `title` VARCHAR(255) NOT NULL COMMENT '电影名',
#   `movie_id` VARCHAR(255) DEFAULT NULL COMMENT '电影id',
#   `rate` FLOAT(11) DEFAULT NULL COMMENT'评分',
#   `url` VARCHAR(255) DEFAULT NULL COMMENT '网址',
#   `cover` VARCHAR(255) DEFAULT NULL COMMENT '封面',
#   `uploadTime` date DEFAULT NULL COMMENT '上映时间',
#   PRIMARY KEY (`Id`)
# ) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COMMENT='豆瓣动漫';

class DoubanPipeline(object):
    def __init__(self):
        self.client =pymysql.Connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='123456',
            db='douban',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor

        )
        self.cur = self.client.cursor()
        self.item_list = []
    def process_item(self, item, spider):
        # self.item_list.append(item)
        # print('len is %s'%len(self.item_list))
        insertStr = "replace into DB_xiju (title,movie_id,rate,url,cover,uploadTime) values ('%s','%s', '%s','%s','%s','%s')"% (item['title'],item['id'],item['rate'],item['url'],item['cover'],item['uploadTime'])
        # print(insertStr)
        # time.sleep(100)
        self.cur.execute(insertStr)
        self.client.commit()
        # if len(self.item_list) >=2:
        #     self.insert_item_list(spider)
    def insert_item_list(self,spider):
        try:
            insertStr = 'insert into DB_xiju (title,movie_id,rate,url,cover,uploadTime)  values'
            for index,item in enumerate(self.item_list):
                print('%s--%s'%(index+1,item['title']))
                itemtr="('%s','%s', '%s','%s','%s','%s')"% (item['title'],item['id'],item['rate'],item['url'],item['cover'],item['uploadTime'])
                if index==len(self.item_list)-1:
                    insertStr+=itemtr+';'
                else:
                    insertStr+=itemtr+','
            print('*****************************')
            print(insertStr)
            if len(insertStr)>80:
                self.cur.execute(insertStr)
                self.client.commit()
            self.item_list=[]
        except Exception as e:
            print('insert_itemList:%s'%e)