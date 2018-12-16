#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tools
import urllib.request
import time
import sys
import os
import di


class Fzdm:

    def __init__(self):
        self.tools = tools.Tools() #工具对象
        self.di = di.Di()
        self.mongodb = self.di.getMongoDb()
        self.co = self.mongodb["fzdm"] # 集合
        self.list_url = "http://manhua.fzdm.com"  # 风之动漫网址

        # 程序运行时间统计
        self.start = time.time()
        self.end = 0

    def cost(self, log=''):
        self.tools.cost(log)

    def run(self):    # 主程序
        self.get_manhua_list()
        # self.get_sub_list()
        self.analyse_sub()
        self.tools.close_browser()
        self.cost("下载完成")

    '''
    获取漫画列表
    '''
    def get_manhua_list(self):
        soup = self.tools.get_dom_obj(self.list_url)
        for block in soup.select(".round"):
            mh_id = block.select("li a")[1].get("href").strip("/")
            sname = block.select("li")[1].string
            surl = self.list_url + "/" + mh_id +"/"
            img = block.select("li a img")[0].get("src")
            title = block.select("li a")[1].get("title")
            mh_info = {
                "_id":mh_id,
                "name": sname,
                "commic_url":surl,
                "img":img,
                "title":title,
                "datetime":self.tools.get_time()
            } 
            self.co["mh_list"].replace_one({"_id":mh_id}, mh_info, True)

    """
    更新所有漫画章节信息
    """
    def get_sub_list(self):  # 获取漫画子列表页面的每一话地址
        for i in self.co["mh_list"].find({}):
            url = i["commic_url"]
            soup = self.tools.get_dom_obj(url)
            li_list = soup.find_all("li", "pure-u-1-2 pure-u-lg-1-4")
            for j in li_list:  # j是每一话的名字和地址
                sub_id = j.a.get("href").strip("/")
                doc_id = i["_id"] +"_"+str(sub_id)
                sub_info = {
                    "_id": doc_id,
                    "sub_url": url + sub_id + "/", 
                    "sub_name": j.a.get("title"),
                    "datetime": self.tools.get_time(),
                    "commic_name": i["name"],
                    "download": False
                }
                self.co["mh_subs"].replace_one({"_id":doc_id}, sub_info, True )

    """
    获取漫画每一话的信息
    """
    def analyse_sub(self):  
        condition = {
            "download": False
        }
        if len(sys.argv) == 3:
            condition["commic_name"] = sys.argv[2]
        for s in self.co["mh_subs"].find(condition):
            self.cost("开始解析" + s['sub_name'])
            page_n = 0  # 页数
            loop = True
            current_url = s['sub_url']  # 当前页面的具体地址
            while loop:
                self.cost("第"+ str(page_n+1) + "页")
                page = self.tools.get_dom_obj(current_url, True)
                pic_url = current_url
                if page:
                    plist = page.select(".navigation a")
                    for i in plist:
                        loop = (i.string == '下一页') # 是否有下一页
                        if loop:
                            current_url = s['sub_url'] + i.get('href')
                            page_n = page_n + 1
                    img = page.find("img", id="mhpic")
                    pic_id = s["_id"] +"_"+ str(page_n)
                    obj = {
                        "_id": pic_id, 
                        "pic_url": pic_url,
                        "pic_src": self.url_filter(img.get('src')),
                        "pic_name": s["sub_name"] + "第"+ str(page_n) + "话",
                        "pic_num": page_n,
                        "commic_name": s["commic_name"],
                        "sub_name": s["sub_name"],
                        "datetime": self.tools.get_time()
                    }
                    self.co["mh_pic"].replace_one({"_id":pic_id}, obj, True)
                else:
                    loop = False
            self.co["mh_subs"].update({"_id":s["_id"]},{"$set":{"download":True}})

            
    def url_filter(self, pic):
        url = pic
        if pic.find('http:') == -1:
            url = 'http:' + pic
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
                self.tools.logging("INFO","pic: %s request is timeout" % obj['pic_src'])
