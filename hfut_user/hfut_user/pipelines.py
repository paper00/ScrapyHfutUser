# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import logging
from twisted.enterprise import adbapi
from scrapy.exceptions import DropItem


class HfutUserPipeline(object):
    def __init__(self, dbPool):
        self.dbPool = dbPool
        self.email = set()

    @classmethod
    def from_settings(cls, settings):
        adbParams = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            port=settings['MYSQL_PORT'],
            database=settings['MYSQL_DATABASE'],
            charset=settings['MYSQL_CHARSET'],
            use_unicode=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        # Connect Pool
        dbPool = adbapi.ConnectionPool('pymysql', **adbParams)

        return cls(dbPool)

    def process_item(self, item, spider):
        # sql -> pool
        query = self.dbPool.runInteraction(self.insert_into, item)
        query.addErrback(self.handle_error)

        return item

    def insert_into(self, cursor, item):
        try:
            sql = """
                        insert users(email) VALUES(%s)
            """
            cursor.execute(sql, (item['email']))
        except Exception as error:
            logging.log(error)
        return item


    def handle_error(self, failure):
        if failure:
            print(failure)