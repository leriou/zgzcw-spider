import di
import tools
import time

class Builder:

    def __init__(self):
        self.tools = tools.Tools()
        self.di = di.Di()
        self.mongodb = self.di.getMongoDb()

        self.list_url = "http://cp.zgzcw.com/lottery/jchtplayvsForJsp.action?lotteryId=47&type=jcmini"
        self.bjop_url = "http://fenxi.zgzcw.com/"

        self.company_list = ["Interwetten","竞彩官方(胜平负)","威廉希尔","伟德(直布罗陀)","立博","澳门","Bet365","香港马会"]
    # 获取url
    def get_module_url(self,module,params):
        if module == "bjop":
            url = self.bjop_url + str(params) +"/bjop"
        elif module == 'list':
            url = self.list_url + "&issue=" + params
        return url

    def run(self):
        self.get_list()

    def get_list(self):
        now = time.time() - (3600 * 12) # 
        n = 0 # 抓取多少天的数据
        loop = True
        while loop:
            date = time.strftime("%Y-%m-%d",time.localtime(now))
            now -= 3600*24
            print(date)
            n += 1
            loop = (n < 100)
            url = self.get_module_url("list",date)
            match_list = self.analysis_list(url)
            if match_list:
                self.mongodb["zgzcw"]["matches"].insert(match_list)
        self.tools.close_browser()
    
    def analysis_list(self,url):
        match_list = []
        if self.tools.check_url_success(url):
            return False
        dom = self.tools.get_dom_obj(url)
        for tr in dom.select(".endBet") + dom.select(".beginBet"):
            odds = {}
            for wh in tr.select(".wh-8 .tz-area"):
                if wh.select("a")[0].text == "未开售":
                    od = {"rq":wh.select(".rq")[0].string,"odds":"未开售"}
                else:     
                    od = {
                        "rq":wh.select(".rq")[0].string,
                        "odds":"",
                        "win":wh.select("a")[0].text,
                        "eq":wh.select("a")[1].text,
                        "lost":wh.select("a")[2].text
                    }
                odds[od["rq"]] = (od)
            bjop = self.get_bjop(tr.select(".wh-10")[0].get("newplayid"))
            match = {
                "competition":tr.get("m"),
                "match_start_time":tr.get("t"),
                "match_date":bjop["match_date"],
                "hostname":tr.select(".wh-4 a")[0].text,
                "visitname":tr.select(".wh-6 a")[0].text,
                "match_score_source":tr.select(".wh-5")[0].string.strip(),
                "host_score":bjop["left_score"],
                "visit_score":bjop["right_score"],
                "match_result":bjop["match_result"],
                "bjop":{
                    "id":tr.select(".wh-10")[0].get("newplayid"),
                    "url":bjop["url"]
                },
                "odds":odds,
                "rates":bjop["rates"]
            }
            match_list.append(match)
        self.tools.marked_url_success(url,True)
        return match_list 

    def get_bjop(self,newplayid):
        url = self.get_module_url("bjop",newplayid)
        return self.analysis_bjop(url)

    def analysis_bjop(self,url):
        dom = self.tools.get_dom_obj(url)
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
                        "win":tds[8].get("data"),
                        "eq":tds[9].get("data"),
                        "lost":tds[10].get("data"),
                    },
                    "kelly_formula":{
                        "win":tds[11].get("data"),
                        "eq":tds[12].get("data"),
                        "lost":tds[13].get("data"),
                    },
                    "odds":tds[14].get("data")
                }
                rate_list[company] = rate_tr
        ret = {
            "url":url,
            "match_date":match_date,
            "match_result":m_ret,
            "left_score":left_score,
            "right_score":right_score,
            "rates":rate_list
        }
        print(host_name + " VS "+ visit_name + " done")
        return ret