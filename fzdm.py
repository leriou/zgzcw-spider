#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tools
import urllib.request
import time
import os
import di


class Fzdm:

    def __init__(self, name=''):
        if name == '':
            print("请输入名称")
        self.commic = {"name":name}
        self.tools = tools.Tools() #工具对象
        self.di = di.Di()
        self.mongodb = self.di.getMongoDb()
        self.redis   = self.di.getRedis()

        self.co = self.mongodb["fzdm"] # 集合
        self.list_url = "http://manhua.fzdm.com"  # 风之动漫网址

        # 程序运行时间统计
        self.start = time.time()
        self.end = 0


    def cost(self, log=''):
        tmp = time.time()
        total, last = tmp - self.start, tmp - self.end
        self.end = tmp
        print("%s 总消耗时间:%s s,距上次%s s" % (log, total, last))

    def run(self):    # 主程序
        url = self.find_from_list(self.commic["name"])
        sub_list = self.get_sub_list(url)
        self.analyse_sub(sub_list)
        self.tools.close_browser()
        self.cost("下载完成")

    def find_from_list(self,name):    # 获取漫画列表地址(http://manhua.fzdm.com/)
        self.cost("开始下载漫画 %s" % self.commic["name"])
        # 检查漫画列表中是否有该漫画的地址
        rec = self.co["mh_list"].find_one(self.commic)
        if rec != None:
            return rec["commic_url"]
        else:   
            soup = self.tools.get_dom_obj(self.list_url)
            mh_info_list = []
            for block in soup.select(".round"):
                sname = block.select("li")[1].string
                surl = self.list_url + "/" + block.select("li a")[1].get("href")
                mh_info = {
                    "name": sname,
                    "commic_url":surl,
                    "datetime":self.tools.get_time()
                } 
                mh_info_list.append(mh_info)
                if sname == name:
                    ret = surl  
            self.co["mh_list"].insert(mh_info_list)
            self.cost("风之动漫列表解析完毕")
            return ret

    def get_sub_list(self,url):  # 获取子列表页面的每一话地址
        soup = self.tools.get_dom_obj(url,True)
        li_list = soup.find_all("li", "pure-u-1-2 pure-u-lg-1-4")
        sublist = []
        for i in li_list:  # i是每一话的名字和地址
            sub_info = {
                "sub_url": url + i.a.get("href"), 
                "sub_name": i.a.get("title"),
                "datetime": self.tools.get_time(),
                "commic_name":self.commic["name"]
            }
            sublist.append(sub_info)  
        if not self.tools.check_url_success(url): 
            self.co["mh_sub_list"].insert(sublist)
            self.tools.marked_url_success(url)
        return sublist

    def analyse_sub(self,sub_list):  # 解析当前这一话的地址 
        for sub in sub_list:
            self.cost("开始解析" + self.commic["name"] + sub['sub_name'])
            n = 0  # 页数
            loop = True
            current_url = sub['sub_url']  # 当前页面的具体地址
            t = time.time()
            while loop:
                page = self.tools.get_dom_obj(current_url,True)
                pic_url = current_url
                if page:
                    plist = page.find_all("a", id="mhona")
                    for i in plist:
                        loop = (i.string == '下一页') # 是否最后一页
                        if loop:
                            current_url = sub['sub_url'] + i.get('href')
                            n = n + 1
                    img = page.find("img", id="mhpic")
                    obj = {
                        "pic_url":pic_url,
                        "pic_src":self.url_filter(img.get('src')),
                        "pic_name":img.get('alt'),
                        "pic_num":n,
                        "commic_name":self.commic["name"],
                        "sub_name":sub["sub_name"],
                        "datetime":self.tools.get_time()
                    }
                    if not self.tools.check_url_success(pic_url):
                        self.co["mh_pic_list"].insert(obj)
                        self.tools.marked_url_success(pic_url)
                else:
                    loop = False
            
    def url_filter(self, pic):
        if pic.find('http:') == -1:
            url = 'http:' + pic
        else:
            url = pic
        return url

    def down_obj(self, obj):  # 下载漫画
        root_dic = self.commic["name"]
        r_path = self.tools.open_dir(root_dic)  # 作品目录
        s_path = os.path.join(r_path, obj['sub_name'])
        if not os.path.isdir(s_path):
            os.mkdir(s_path)
       
        filename = s_path + "/" + obj['sub_name'] + "_" + str(obj['pic_num']) + ".jpg"
        if not os.path.exists(filename):
            try:
                pic = obj["pic_src"]
                urllib.request.urlretrieve(pic, filename)
            except:
                print("pic: %s request is timeout" % obj['pic_src'])
