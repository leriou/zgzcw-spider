#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import os
from bs4 import BeautifulSoup
import logging


class Tools:

    # 从url获取页面内容
    def get_html(self, url):
        try:
            times = 3
            while times > 0:
                data = urllib.request.urlopen(url)
                code = data.code
                times = times - 1
                if code == 200:
                    times = False
            if code == 200:
                data = data.read().decode("utf-8")
                return data
            else:
                return False
        except:
            return False

    def get_dom_obj_by_content(self,html):
        return BeautifulSoup(html,'html.parser')

    # 获取页面的dom对象
    def get_dom_obj(self, url):
        data = self.get_html(url)
        if data:
            return self.get_dom_obj_by_content(data)
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

    def logging(self,log):
        logger = logging.getLogger("Tools")
        print(log)
        logger.info(log)

