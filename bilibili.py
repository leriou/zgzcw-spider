import di
import tools
from selenium import webdriver
import time,sys

class Bilibili:
    
    def __init__(self):
        self.tools = tools.Tools()
        self.di = di.Di()
        self.mongodb = self.di.getMongoDb()
        self.tools.cache = self.mongodb["bilibili"]["local_url_cache"]
        self.user_db = self.mongodb["bilibili"]['users']
       
    # url map
    def url_map(self,flag,id):
        if flag == 'user':
            return "https://space.bilibili.com/" + str(id)+"#/"

    def close_browser(self):
        self.tools.close_browser()

    # 获取某个用户的信息
    def get_user_info(self,url,save_user = True):
        if self.tools.check_url_success(url):
            return False
        dom = self.tools.get_dom_obj(url)
        # 解析dom页面
        avatar = dom.select("#h-avatar")[0].get("src")
        username = dom.select("#h-name")[0].string
        level = dom.select(".h-level")[0].get("lvl")
        gender = dom.select("#h-gender")[0].get("class")
        if len(gender) == 3:
            gender = gender[2]
        else:
            gender = ""
        vip = dom.select(".h-vipType")[0].get("class")
        if len(vip) == 2:
            if vip[1] == 'normal-v':
                vip = "大会员"
            else:
                vip = "年费大会员"
        elif len(vip) == 1:
            vip = "否"

        sign = dom.select(".h-sign")[0].string.strip()
        uid = dom.select(".user .uid .text")[0].string.strip()
        regtime =  dom.select(".user .regtime .text")[0].string.strip().strip("注册于 ")
        birthday = dom.select(".user .birthday .text")[0].string.strip()
        videos = dom.select(".n-video .n-num")[0].string 
        favlist = dom.select(".n-favlist .n-num")[0].string.strip()
        focus =dom.select(".n-statistics .n-gz")[0].get("title").replace(",","")  
        fans = dom.select(".n-statistics .n-fs")[0].get("title").replace(",","")
        plays = 0
        if dom.select(".n-statistics .n-bf"):
            plays = dom.select(".n-statistics .n-bf")[0].get("title").replace(",","")
        user_info = {
            "avatar":avatar,
            "username":username,
            "gender":gender,
            "level":level,
            "vip":vip,
            "sign":sign,
            "uid":uid,
            "regtime":regtime,
            "birthday":birthday,
            "videos":videos,
            "favlist":favlist,
            "focus":focus,
            "fans":fans,
            "plays":plays
        }   
        self.tools.logging("INFO",user_info)
        if save_user:
            self.save_user_info(user_info)
        return user_info
        
    def save_user_info(self,user_info):
        self.user_db.insert(user_info)
    
    def run(self):
        uid = 1
        if len(sys.argv) >= 3:
            uid = sys.argv[2]
        url = self.url_map("user",uid)
        user_info = self.get_user_info(url)
        if user_info:
            self.tools.marked_url_success(url)
        self.close_browser()
