#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/12/28 18:56
# @Author : LiangJiangHao
# @Software: PyCharm

# -*- coding: utf-8 -*-
#!DATE: 2018/7/15 13:26
#!@Author: yy
import sys
import MySQLdb

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class CncompanyidSpiderFastPipeline(object):
    companylist = []

    def open_spider(self, spider):
        self.conn = MySQLdb.connect(host="***", user="***", passwd="***",db="***",charset="utf8")
        self.cursor = self.conn.cursor()
        # 存入数据之前清空表：
        self.cursor.execute("truncate table cn_companyid")
        self.conn.commit()

    # 批量插入mysql数据库
    def bulk_insert_to_mysql(self, bulkdata):
        try:
            print "the length of the data-------", len(self.companylist)
            sql = "insert into cn_companyid (id, name) values(%s, %s)"
            self.cursor.executemany(sql, bulkdata)
            self.conn.commit()
        except:
            self.conn.rollback()

    def process_item(self, item, spider):
        self.companylist.append([item['CompanyID'], item['Companyname']])
        if len(self.companylist) == 1000:
            self.bulk_insert_to_mysql(self.companylist)
            # 清空缓冲区
            del self.companylist[:]
        return item

    def close_spider(self, spider):
        print "closing spider,last commit", len(self.companylist)
        self.bulk_insert_to_mysql(self.companylist)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()