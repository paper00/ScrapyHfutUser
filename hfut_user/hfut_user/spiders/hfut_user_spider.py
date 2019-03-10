# -*- coding: utf-8 -*-
import scrapy
import requests
from hfut_user.items import HfutUserItem
import execjs
import json

class HfutUserSpiderSpider(scrapy.Spider):
    name = 'hfut_user_spider'
    allowed_domains = ['jxglstu.hfut.edu.cn']
    salt_url = 'http://jxglstu.hfut.edu.cn/eams5-student/login-salt'
    login_url = 'http://jxglstu.hfut.edu.cn/eams5-student/login'
    start_urls = ['http://jxglstu.hfut.edu.cn/eams5-student/my/profile',
                  'http://jxglstu.hfut.edu.cn/eams5-student/for-std/student-info']
    salt = ''
    cookie_dict = {}
    hfutUserItem = HfutUserItem()

    def stringToDict(self, cookie):
        itemDict = {}
        items = cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict

    def get_sha1(self):
        f = open("./sha1.js", 'r', encoding='UTF-8')
        line = f.readline()
        htmlstr = ''
        while line:
            htmlstr = htmlstr + line
            line = f.readline()
        return htmlstr

    def start_requests(self):
        # Login-salt
        self.salt = requests.get(self.salt_url)
        yield scrapy.Request(self.login_url, callback=self.login, dont_filter=True)

    def login(self, response):
        # Username
        username = "2017214***"
        # Password
        password = self.salt.text + '-' + '******'
        sha1 = self.get_sha1()
        ctx = execjs.compile(sha1)
        encryptPassword = ctx.call("f", password) + ""
        # Cookie
        cookie = self.salt.headers["Set-Cookie"].split(';')[0]
        self.cookie_dict = self.stringToDict(cookie)
        # Headers
        headers = {
            "Content-Type": "application/json",
            "Cookie": cookie
        }
        # FormData
        data = {
            'username': username,
            'password': encryptPassword,
            'captcha': '',
        }

        # Login
        html = requests.post(self.login_url, data=json.dumps(data), headers=headers)

        yield scrapy.Request(''.join(self.start_urls[0]), cookies=self.cookie_dict, callback=self.parse_info1)

    def parse_info1(self, response):
        # Test
        target_page = ''.join(self.start_urls[0])
        if response.url == target_page:
            print("Successfully accessed user's profile page.")
        else:
            print('Login faild.')

        # Save to Item pt.1
        form_xpath = response.xpath("//div[@class='col-sm-offset-3 col-sm-6']")
        self.hfutUserItem['name'] = form_xpath.xpath("./div[1]/div[2]/span/text()").extract()
        self.hfutUserItem['sex'] = form_xpath.xpath("./div[2]/div[2]/span/text()").extract()
        self.hfutUserItem['id'] = form_xpath.xpath("./div[4]/div[2]/span/text()").extract()
        self.hfutUserItem['birthday'] = form_xpath.xpath("./div[5]/div[2]/span/text()").extract()
        self.hfutUserItem['email'] = form_xpath.xpath("./div[7]/div[2]/span/text()").extract()
        self.hfutUserItem['phone'] = form_xpath.xpath("./div[11]/div[2]/span/text()").extract()

        yield scrapy.Request(''.join(self.start_urls[1]), cookies=self.cookie_dict, callback=self.parse_info2)

    def parse_info2(self, response):
        # Save to Item pt.2
        self.hfutUserItem['department'] = response.xpath("//dl//dd[6]/text()").extract()
        self.hfutUserItem['major'] = response.xpath("//dl//dd[9]/text()").extract()

        print(self.hfutUserItem)
        yield self.hfutUserItem
