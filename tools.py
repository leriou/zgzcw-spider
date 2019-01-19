#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from pymongo import MongoClient
import random


class Tools:
    
    def __init__(self):
        self.browser = None
        self.sleep = False
        self.rand_floor = 0
        self.rand_ceil = 3
        self.start = time.time()
        self.end = time.time()
        self.mongo = None
    
    def get_mongodb(self):
        if self.mongo == None:
            self.mongo = MongoClient('127.0.0.1', 27017)
        return self.mongo
    
    def set_cache(self, db, collection):
        self.cache = self.mongo[db][collection]
    
    # 从url获取页面内容
    def get_html(self, url):
        try:
            times = 3    
            while times > 0:
                param_data = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}
                response = requests.get(url, params=param_data)
                times -= 1
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
    def browser_get_html(self, url):
        if self.browser == None:
            self.browser = webdriver.Chrome()     
        if self.sleep:
            time.sleep(self.get_random_num(self.rand_floor, self.rand_ceil))
        self.browser.get(url)
        return self.browser.page_source

    def mongo_set(self, url, data):
        r = self.cache.find_one({"_url": url})
        if r:
            self.cache.update({"_url":url}, {"$set":data})
        else:
            data["_url"] = url
            data["datetime"] = self.get_time()
            data["timestamp"] = time.time()
            self.cache.insert_one(data)
        
    def mongo_get(self,url):
        return self.cache.find_one({"_url":url})

    def mongo_clear_cache(self):
        self.cache.update_many({},{"$set":{"text":""}})

    # 从html字符串获取dom对象
    def get_dom_by_html(self,html):
        if html == None:
            return False
        return BeautifulSoup(html, 'html.parser')

    # 标记某个url处理成功
    def marked_url_success(self,url,flag = 1):
        self.mongo_set(url,{"success":flag})

    # 检查某个url是否成功
    def check_url_success(self,url):
        r = self.mongo_get(url)
        if r and r.get("success"):
            return r["success"]
        return False

    # 获取页面的dom对象如果页面被缓存使用缓存
    def get_dom_obj(self, url, cached=True, browser=True):
        if cached:
            r = self.mongo_get(url)
            if r != None and r.get("text") :
                return self.get_dom_by_html(r["text"])
        if browser:
            data = self.browser_get_html(url)
        else:
            data = self.get_html(url)
        if data:
            if cached:
                self.mongo_set(url,{"text":data}) 
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
    def log_to_file(self,filename,content):
        with open(filename,"w+") as fh:
            fh.write(content)

    def get_time(self):
        return self.time2str(time.time())
    
    def str2time(self, i):
        return time.mktime(time.strptime(i,"%Y-%m-%d %H:%M:%S"))
    
    def time2str(self, moment):
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(moment))
        
    def cost(self, log=''):
        tmp = time.time()
        total, last = tmp - self.start, tmp - self.end
        self.end = tmp
        self.logging("INFO","%s cost time: %s s, until lastest %s s" % (log, total, last))

    def logging(self, level, msg):
        print("%s [%s]: %s" % (self.get_time(),level,msg))

    def get_random_num(self, start=0, end=1):
        return random.random() * (end - start) + start