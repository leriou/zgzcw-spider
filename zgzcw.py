import tools
import time
import sys
import os

class Zgzcw:

    def __init__(self):
        self.tools = tools.Tools()

        self.dbname = "zgzcw"
        self.cache_collection = "tmp-url"
        self.data_collection = "data"
        self.log_collection = "log"
        
        """
            params:
            offset_time: 从当前时间多久前开始抓数据, 今天的比赛还没有出结果
            limit_day: 抓取多少天然后停止
        """
        self.offset_time = 3600 * 24 * 5 
        self.limit_day = 365 * 5 

    def _init_data(self):
        self.list_url = "http://cp.zgzcw.com/lottery/jchtplayvsForJsp.action?lotteryId=47&type=jcmini"
        self.bjop_url = "http://fenxi.zgzcw.com/"
        self.company_list = ["Interwetten","竞彩官方(胜平负)","威廉希尔","伟德(直布罗陀)","立博","澳门","Bet365","香港马会"]

        self.mongodb = self.tools.get_mongodb()
        self.tools.set_cache(self.dbname, self.cache_collection)
        self.db    = self.mongodb[self.dbname][self.data_collection]
        self.logdb = self.mongodb[self.dbname][self.log_collection]
        
    # 获取url
    def get_module_url(self, module, params):
        if module == "bjop":
            url = self.bjop_url + str(params) +"/bjop"
        elif module == 'list':
            url = self.list_url + "&issue=" + params
        return url

    def run(self):
        if len(sys.argv) >= 2:
            date = sys.argv[1]
        else:
            date = None
        self._init_data()
        self.get_list(date)

    def get_list(self,date = None):
        if date != None:
            self.get_list_by_date(date)
        else:
            now = time.time() - self.offset_time 
            limit = self.limit_day
            loop = True
            while loop:
                date = time.strftime("%Y-%m-%d", time.localtime(now))
                now -= 3600*24
                limit -= 1
                loop = (limit > 0)
                if not self.date_has_done(date):
                    self.get_list_by_date(date)
        self.tools.close_browser()
    
    def get_list_by_date(self,date):
        self.tools.logging("INFO","------"+ date + "------")
        url = self.get_module_url("list", date)
        match_list = self.analysis_list(url)
        if match_list:
            self.db.insert_many(match_list)
            log_info = {
                "date":    date,
                "success": True,
                "count":   len(match_list),
                "time":    self.tools.get_time()
            }
            self.logdb.replace_one({"date":date}, log_info, True)
            self.tools.cost("处理%s数据%s条" % (date, len(match_list)))
            self.tools.mongo_clear_cache()
    
    def analysis_list(self,url):
        match_list = []
        if self.tools.check_url_success(url):
            return False
        dom = self.tools.get_dom_obj(url)
        for tr in dom.select(".endBet") + dom.select(".beginBet"):    
            bjop = self.get_bjop(tr.select(".wh-10")[0].get("newplayid"))
            if bjop:
                odds = {}
                for wh in tr.select(".wh-8 .tz-area"):
                    if wh.select("a")[0].text == "未开售":
                        od = {"rq":wh.select(".rq")[0].string,"odds":False}
                    else:     
                        od = {
                            "rq":wh.select(".rq")[0].string,
                            "odds":True,
                            "win":wh.select("a")[0].text,
                            "eq":wh.select("a")[1].text,
                            "lost":wh.select("a")[2].text
                        }
                    odds[od["rq"]] = (od)       
                match = {
                    "competition":tr.get("m"),
                    "list_url":url,
                    "match_start_time":tr.get("t"),
                    "match_date":bjop["match_date"],
                    "hostname":tr.select(".wh-4 a")[0].text,
                    "visitname":tr.select(".wh-6 a")[0].text,
                    "match_score_source":tr.select(".wh-5")[0].string.strip(),
                    "host_score":bjop["left_score"],
                    "visit_score":bjop["right_score"],
                    "match_result":bjop["match_result"],
                    "created_time":self.tools.get_time(),
                    "bjop":{
                        "id":tr.select(".wh-10")[0].get("newplayid"),
                        "url":bjop["url"]
                    },
                    "odds":odds,
                    "rates":bjop["rates"],
                    "estimate":self.estimate(bjop["rates"])
                }
                match_list.append(match)
        self.tools.marked_url_success(url, True)
        return match_list 



    def analysis_bjop(self,url):
        if self.check_bjop_done(url):
            return False
        dom = self.tools.get_dom_obj(url)
        if len(dom.select(".logoVs .host-name a")) == 0:
            return False
        host_name = dom.select(".logoVs .host-name a")[0].string
        visit_name = dom.select(".logoVs .visit-name a")[0].string
        match_date = dom.select(".bfyc-duizhen-r .date span")[0].string
        match_score =  dom.select(".vs-score span")
        if len(match_score) == 0:
            left_score = right_score = 0
        else:
            left_score  = match_score[0].string
            right_score = match_score[1].string
        if left_score == right_score:
            m_ret = 1
        elif left_score > right_score:
            m_ret = 3
        elif left_score < right_score:
            m_ret = 0
        t_rate_list =  dom.select(".tr-hr")
        rate_list = {}
        for tr in t_rate_list:
            tds = tr.select("td")
            company = tds[1].contents[1]
            if company in self.company_list:
                rate_tr = {
                    "begin":{
                        "win":tds[2].get("data"),
                        "eq":tds[3].get("data"),
                        "lost":tds[4].get("data")
                    },
                    "latest":{
                        "win":tds[5].get("data"),
                        "eq":tds[6].get("data"),
                        "lost":tds[7].get("data")
                    },
                    "probability":{
                        "win":tds[9].get("data"),
                        "eq":tds[10].get("data"),
                        "lost":tds[11].get("data"),
                    },
                    "kelly_formula":{
                        "win":tds[12].get("data"),
                        "eq":tds[13].get("data"),
                        "lost":tds[14].get("data"),
                    },
                    "odds":tds[15].get("data")
                }
                rate_list[company] = rate_tr
        ret = {
            "url":url,
            "match_date":match_date,
            "match_result":m_ret,
            "left_score":left_score,
            "right_score":right_score,
            "rates":rate_list,
        }
        self.tools.logging("INFO",host_name + " VS "+ visit_name + ": success")
        return ret

    def get_bjop(self, newplayid):
        return self.analysis_bjop(self.get_module_url("bjop", newplayid))
    
    def check_bjop_done(self,url):
        return self.db.find_one({"bjop.url":url})

    def date_has_done(self, date):
        return self.logdb.find_one({"date": date})

    def estimate(self, data): # 根据历史记录统计某赔率下的胜率
        arr = ["Interwetten","竞彩官方(胜平负)"]
        rt = {}
        for key in arr:
            if data.get(key):
                rs = self.mongodb["zgzcw"]["matches"].find({
                    "rates."+key+".begin":data[key]["begin"]
                })
                ret = {
                    "0":0,
                    "1":0,
                    "3":0
                }
                for r in rs:
                    ret[str(r["match_result"])] += 1
                rt[key] = ret
        return rt
                
        
        
