# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import time
from twisted.enterprise import adbapi
# 同步插入
# class AcfunPipeline(object):
#     def __init__(self):
#         self.client =pymysql.Connect(
#             host='127.0.0.1',
#             port=3306,
#             user='root',
#             passwd='123456',
#             db='ac_up',
#             charset='utf8mb4',
#             cursorclass=pymysql.cursors.DictCursor
#
#         )
#         self.cur = self.client.cursor()
#     def process_item(self, item, spider):
#         sql = "REPLACE into up_baseInfor (userid,userImg,user_name,followed,bananaGold)  values ('%s','%s', '%s','%s','%s')" % (item['userId'],item['userImg'],item['userName'],item['fenceNum'],item['bananaGold'])
#         self.cur.execute(sql)
#         self.client.commit()
#         return item
# ******************************************************************
# 异步
# 数据库pymysql的commit()和execute()在提交数据时，都是同步提交至数据库，由于scrapy框架数据的解析是异步多线程的，所以scrapy的数据解析速度，要远高于数据的写入数据库的速度。如果数据写入过慢，会造成数据库写入的阻塞，影响数据库写入的效率。
# 通过多线程异步的形式对数据进行写入，可以提高数据的写入速度。
# class AcfunPipeline(object):
#     def __init__(self, dbpool):
#         self.dbpool = dbpool
#     @classmethod
#     def from_settings(cls, settings):
#         params = dict(
#             host=settings['MYSQL_HOST'],
#             db=settings['MYSQL_DB'],
#             user=settings['MYSQL_USER'],
#             passwd=settings['MYSQL_PASSWD'],
#             charset=settings['MYSQL_CHARSET'],
#             port=settings['MYSQL_PORT'],
#             cursorclass=pymysql.cursors.DictCursor
#         )
#         # 初始化数据库连接池(线程池)
#         # 参数一：mysql的驱动
#         # 参数二：连接mysql的配置信息
#         dbpool = adbapi.ConnectionPool('pymysql', **params)
#         return cls(dbpool)
#
#     def process_item(self, item, spider):
#         # 在该函数内，利用连接池对象，开始操作数据，将数据写入到数据库中。
#         # pool.map(self.insert_db, [1,2,3])
#         # 同步阻塞的方式： cursor.execute() commit()
#         # 异步非阻塞的方式
#         # 参数1：在异步任务中要执行的函数insert_db；
#         # 参数2：给该函数insert_db传递的参数
#         query = self.dbpool.runInteraction(self.insert_db, item)
#
#         # 如果异步任务执行失败的话，可以通过ErrBack()进行监听, 给insert_db添加一个执行失败的回调事件
#         query.addErrback(self.handle_error)
#
#         return item
#
#     def handle_error(self, field):
#         print('-----数据库写入失败：', field)
#
#     def insert_db(self, cursor, item):
#         insert_sql = "REPLACE into up_baseInfor (userid,userImg,user_name,followed,bananaGold)  values ('%s','%s', '%s','%s','%s')" % (item['userId'],item['userImg'],item['userName'],item['fenceNum'],item['bananaGold'])
#         cursor.execute(insert_sql)

class AcfunPipeline(object):
    def __init__(self):
        self.client =pymysql.Connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='123456',
            db='ac_up',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor

        )
        self.cur = self.client.cursor()
        self.item_list = []
    def process_item(self, item, spider):
        self.item_list.append(item)
        # print('len is %s'%len(self.item_list))
        if len(self.item_list) >=10000:
            self.insert_item_list(spider)
    def insert_item_list(self,spider):
        try:
            insertStr = 'insert into up_baseInfor (userid,userImg,user_name,followed,bananaGold)  values'
            for index,item in enumerate(self.item_list):
                print('%s--%s'%(index+1,item['userName']))
                itemtr="('%s','%s', '%s','%s','%s')"% (item['userId'],item['userImg'],item['userName'],item['fenceNum'],item['bananaGold'])
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
            # time.sleep(100)
# 查询是否有这条数据
            # selectSql='select *from up_baseInfor where userid="%s"'%item['userId']
            # self.cur.execute(selectSql)
            # data=self.cur.fetchall()
            # print(len(data))
        #     if len(data)==0:
        #         itemtr="('%s','%s', '%s','%s','%s')"% (item['userId'],item['userImg'],item['userName'],item['fenceNum'],item['bananaGold'])
        #         if index==len(self.item_list)-1:
        #             insertStr+=itemtr+';'
        #         else:
        #             insertStr+=itemtr+','
        #     else:
        #         continue