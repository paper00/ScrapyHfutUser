# -*- coding: utf-8 -*-

from hashlib import sha1
from scrapy import cmdline
import execjs
import requests
import json
import importlib,sys
importlib.reload(sys)

cmdline.execute('scrapy crawl hfut_user_spider'.split())