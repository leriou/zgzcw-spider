#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import os
import di
import time
from bs4 import BeautifulSoup
from selenium import webdriver

class Tools:
    
    def __init__(self):
        self.di = di.Di()
        self.redis = self.di.getRedis()
        self.mongo = self.di.getMongoDb()
        self.browser = None

        self.start = time.time()
        self.end = 0

    # 从url获取页面内容
    def get_html(self, url):
        try:
            times = 3    
            while times > 0:
                param_data = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}
                response = requests.get(url,params=param_data)
                times = times - 1
                if response.status_code == 200:
                    times = False
            if response.status_code == 200:
                response.encoding = 'utf-8'
                return response.text
            else:
                return False
        except:
            return False

    # 关闭浏览器
    def close_browser(self):
        if self.browser != None:
            self.browser.close()

    # 浏览器获取
    def browser_get_html(self,url):
        if self.browser == None:
            self.browser = webdriver.Firefox()
        self.browser.get(url)
        return self.browser.page_source

    # 从html字符串获取dom对象
    def get_dom_by_html(self,html):
        if html == None:
            return False
        return BeautifulSoup(html, 'html.parser')

    # 标记某个url处理成功
    def marked_url_success(self,url,flag = 1):
        self.redis.set("html:success:"+url,flag)

    # 检查某个url是否成功
    def check_url_success(self,url):
        return self.redis.get("html:success:"+url)

    # 获取页面的dom对象如果页面被缓存使用缓存
    def get_dom_obj(self, url, cached=True,browser=True):
        if cached:
            html = self.redis.get(url) # 获取缓存
            if html != None :
                return self.get_dom_by_html(html)
        if browser:
            data = self.browser_get_html(url)
        else:
            data = self.get_html(url)
        if data:
            if cached:
                self.redis.set(url,data)  
            return self.get_dom_by_html(data)
        else:
            return False

    # 打开文件夹
    def open_dir(self, name):
        now = os.path.abspath('.')
        newpath = os.path.join(now, name)
        if os.path.isdir(newpath):
            return newpath
        else:
            os.mkdir(newpath)
            return newpath

    # 往某文件写入内容
    def log(self,filename,content):
        fh = open(filename,"w+")
        fh.write(content)
        fh.close()

    def get_time(self):
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        
    def cost(self, log=''):
        tmp = time.time()
        total, last = tmp - self.start, tmp - self.end
        self.end = tmp
        print("%s 总消耗时间:%s s,距上次%s s" % (log, total, last))