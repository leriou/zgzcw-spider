#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import re
import os
import time
import requests
from bs4 import BeautifulSoup


class Tools:

    def getHtml(self, url):
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

    def getDomObj(self, url):
        data = self.getHtml(url)
        if data:
            return BeautifulSoup(data, 'html.parser')
        else:
            return 0

    def openDir(self, name):
        now = os.path.abspath('.')
        newpath = os.path.join(now, name)
        if os.path.isdir(newpath):
            return newpath
        else:
            os.mkdir(newpath)
            return newpath


class Manhua:

    def __init__(self):
        self.start = time.time()  # 开始时间
        self.end = self.start  # 断点
        self.tools = Tools()
        self.url = ''  # 漫画地址
        self.name = ''  # 漫画名字
        self.sublist = ''  # 每一话的详情
        self.piclist = ''  # 图片
        self.timeout = 1000

    def down(self, name):
        self.name = name
        url = self.getManhuaUrl(name)
        self.download(url)

    def download(self, url):
        print("start down:%s\n" % self.name)
        sublist = self.getSubList(url)
        for i in sublist:
            self.downSubs(i)

    def getManhuaUrl(self, name):
        url = "http://manhua.fzdm.com"
        soup = self.tools.getDomObj(url)
        title = name + "漫画"
        href = url + "/" + soup.find("a", title=title).get('href')
        self.url = href
        return href

    def cost(self, act):
        tmp = time.time()
        total = tmp - self.start
        last = tmp - self.end
        self.end = tmp
        print("%s总消耗时间:%s s,距上次%s s" % (act, total, last))

    def getSubList(self, url):
        soup = self.tools.getDomObj(url)
        lilist = soup.find_all("li", "pure-u-1-2 pure-u-lg-1-4")
        sublist = []
        for i in lilist:
            url = self.url + i.a.get("href")
            name = i.a.get("title")
            subs = {"url": url, "name": name}
            sublist.append(subs)
        self.sublist = sublist
        return sublist

    def getPicUrl(self, url):
        piclist = []
        for i in range(0, 1000):
            tmp = {}
            page = url + "index_" + str(i) + ".html"
            obj = self.tools.getDomObj(page)
            if obj:
                tmp['name'] = "第" + str(i + 1) + "页"
                tmp['pic'] = obj.find("img", id="mhpic").get("src")
                piclist.append(tmp)
            else:
                return piclist

    def downSubs(self, subs):
        pages = self.getPicUrl(subs['url'])
        name = subs['name']
        detail = {"name": name, "list": pages}
        self.downObj(detail)

    def downObj(self, obj):
        r_path = self.tools.openDir(self.name)  # 作品目录
        self.cost("开始下载%s %s" % (self.name, obj['name']))
        s_path = os.path.join(r_path, obj['name'])
        if not os.path.isdir(s_path):
            os.mkdir(s_path)
        for j in obj['list']:
            filename = s_path + "/" + j['name'] + ".jpg"
            if not os.path.exists(filename):
                try:
                    test = urllib.request.urlopen(j['pic'], timeout=self.timeout).code
                    if test == 200:
                        urllib.request.urlretrieve(j['pic'], filename)
                except:
                    print("%s请求超时" % j['pic'])


if __name__ == "__main__":
    name = "虫姬"
    m = Manhua()
    m.down(name)
