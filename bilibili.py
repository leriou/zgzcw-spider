import di
import tools
from selenium import webdriver

class Builder:
    
    def __init__(self):
        self.tools = tools.Tools()
        self.di = di.Di()
        self.mongodb = self.di.getMongoDb()
       
    # url map
    def url_map(self,flag,id):
        if flag == 'user':
            return "https://space.bilibili.com/" + str(id)

    def close_browser(self):
        self.tools.close_browser()

    # 获取某个用户的信息
    def get_user_info(self,uid):
        url = self.url_map("user",uid)
        dom = self.tools.get_dom_obj(url)
        # 解析dom页面
        avatar = dom.select("#h-avatar")[0].get("src")
        user_name = dom.select("#h-name")[0].string
        level = dom.select(".h-level")[0].get("lvl")
        
        gender = dom.select("#h-gender")[0].get("class")
        if len(gender) == 3:
            if gender[2] == 'female':
                gender = "女"
            elif gender[2] == 'male':
                gender = "男"
        else:
            gender = "未知"
        vip = dom.select(".h-vipType")[0].get("class")
        if len(vip) == 2:
            if vip[1] == 'normal-v':
                vip = "大会员"
            else:
                vip = "年费大会员"
        elif len(vip) == 1:
            vip = "否"
        sign = dom.select(".h-sign")[0].string.strip()
        uid = dom.select(".section .uid span")[1].string
        reg_time =  dom.select(".section .regtime span")[1].string.strip()
        birthday = dom.select(".section .birthday span")[1].string.strip()
        address =  dom.select(".section .geo span")[1].string.strip()
        videos = dom.find(href="#/video").select("span")[2].string # 投稿

        n_statistics = dom.select(".n-statistics")[0]
        focus =  n_statistics.select("#n-gz")[0].string  # 关注数
        fans =   n_statistics.select("#n-fs")[0].string  # 粉丝数
        if len(n_statistics.select("#n-bf")) == 1:
            plays = n_statistics.select("#n-bf")[0].string   # 播放数
        else:
            plays = 0
            
        user_info = {
            "avatar":avatar,
            "username":user_name,
            "gender":gender,
            "level":level,
            "vip":vip,
            "sign":sign,
            "uid":uid,
            "regtime":reg_time,
            "birthday":birthday,
            "address":address,
            "videos":videos,
            "focus":focus,
            "fans":fans,
            "plays":plays
        }
        self.close_browser()
        return user_info
        
    def save_user_info(self,user_info):
        self.mongodb["users"]['bilibili'].insert(user_info)
    
    def run(self):
        user_info = self.get_user_info(12355)  
        self.save_user_info(user_info)
        print(user_info)
