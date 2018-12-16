import di
import tools
from selenium import webdriver
import time,sys

class Bilibili:
    
    def __init__(self):
        self.tools = tools.Tools()
        self.di = di.Di()
        self.mongodb = self.di.getMongoDb()
        self.redis = self.di.getRedis()
        self.tools.cache = self.mongodb["bilibili"]["local_url_cache"]
        self.user_db = self.mongodb["bilibili"]['users']
       
    # url map
    def url_map(self,flag,id):
        if flag == 'user':
            return "https://space.bilibili.com/" + str(id)

    def close_browser(self):
        self.tools.close_browser()

    # 获取某个用户的信息
    def get_user_info(self,url,save_user = True):
        if self.tools.check_url_success(url):
            return False
        dom = self.tools.get_dom_obj(url, False)
        # 解析dom页面
        user_info = {}
        if dom.select("#h-avatar"):
            user_info["avatar"] = dom.select("#h-avatar")[0].get("src")
        if dom.select("#h-name"):
            user_info["username"] = dom.select("#h-name")[0].string
        if dom.select(".h-level"):
            user_info["level"] = dom.select(".h-level")[0].get("lvl")
        if dom.select("#h-gender"):
            gender = dom.select("#h-gender")[0].get("class")
            if len(gender) == 3:
                user_info["gender"] = gender[2]
            else:
                user_info["gender"] = ""
        if dom.select(".h-vipType"):
            vip = dom.select(".h-vipType")[0].get("class")
            if len(vip) == 2:
                if vip[1] == 'normal-v':
                    vip = "大会员"
                else:
                    vip = "年费大会员"
            elif len(vip) == 1:
                vip = "否"
            user_info["vip"] = vip
        if dom.select(".h-sign"):
            user_info["sign"] = dom.select(".h-sign")[0].string.strip()
        if dom.select(".user .uid .text"):
            user_info["_id"] = dom.select(".user .uid .text")[0].string.strip()
        if dom.select(".user .regtime .text"):
            user_info["regtime"] =  dom.select(".user .regtime .text")[0].string.strip().strip("注册于 ")
        if dom.select(".user .birthday .text"):
            user_info["birthday"] = dom.select(".user .birthday .text")[0].string.strip()
        if dom.select(".n-video .n-num"):
            user_info["videos"] = dom.select(".n-video .n-num")[0].string 
        if dom.select(".n-favlist .n-num"):
            user_info["favlist"] = dom.select(".n-favlist .n-num")[0].string.strip()
        if dom.select(".n-statistics .n-gz"):
            user_info["focus"] = dom.select(".n-statistics .n-gz")[0].get("title").replace(",","")  
        if dom.select(".n-statistics .n-fs"):
            user_info["fans"] = dom.select(".n-statistics .n-fs")[0].get("title").replace(",","")
        plays = 0
        if dom.select(".n-statistics .n-bf"):
            plays = dom.select(".n-statistics .n-bf")[0].get("title").replace(",","")
        user_info["plays"] = plays
        self.tools.logging("INFO",user_info)
        if save_user:
            self.save_user_info(user_info)
        return user_info
        
    def save_user_info(self,user_info):
        self.user_db.replace_one({"_id": user_info["_id"]} , user_info, True)
    
    def run(self):
        uid = 1
        loop = True
        while loop:
            if len(sys.argv) == 3:
                uid = int(sys.argv[2])
                loop = False
            url = self.url_map("user", uid)
            time.sleep(2)
            uid = uid + 1
            user_info = self.get_user_info(url)
            if user_info:
                self.tools.marked_url_success(url)
        self.close_browser()
