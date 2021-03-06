# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HfutUserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    sex = scrapy.Field()
    id = scrapy.Field()
    birthday = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    department = scrapy.Field()
    major = scrapy.Field()
