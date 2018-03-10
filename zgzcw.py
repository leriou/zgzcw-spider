import di
import tools
import time

class Builder:

    def __init__(self):
        self.tools = tools.Tools()
        self.di = di.Di()
        self.redis = self.di.getRedis()
        self.mongodb = self.di.getMongoDb()

        self.list_url = "http://cp.zgzcw.com/lottery/jchtplayvsForJsp.action?lotteryId=47&type=jcmini"
        self.bjop_url = "http://fenxi.zgzcw.com/"


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
        url = self.get_module_url("list","2018-03-07")
        match_list = self.analysis_list(url)
        self.mongodb["zgzcw"]["matches"].insert(match_list)
        self.tools.close_browser()
    
    def analysis_list(self,url):
        match_list = []
        dom = self.tools.get_dom_obj(url)
        for tr in dom.select(".endBet") + dom.select(".beginBet"):
            odds = []
            for wh in tr.select(".wh-8 .tz-area"):
                if wh.select("a")[0].text == "未开售":
                    od = {
                        "rq":wh.select(".rq")[0].string,
                        "odds":"未开售"
                    }
                else:     
                    od = {
                        "rq":wh.select(".rq")[0].string,
                        "odds":"",
                        "win":wh.select("a")[0].text,
                        "eq":wh.select("a")[1].text,
                        "failed":wh.select("a")[2].text
                    }
                odds.append(od)
            match = {
                "competition":tr.get("m"),
                "match_start_time":tr.get("t"),
                "hostname":tr.select(".wh-4 a")[0].string,
                "visitname":tr.select(".wh-6 a")[0].string,
                "match_score":tr.select(".wh-5")[0].string.strip(),
                "bjopid":tr.select(".wh-10")[0].get("newplayid"),
                "odds":odds
            }
            match_list.append(match)
        return match_list 

    def analysis_bjop(self,dom):
        host_name = dom.select(".logoVs .host-name a")[0].string
        visit_name = dom.select(".logoVs .visit-name a")[0].string
        match_date = dom.select(".bfyc-duizhen-r .date span")[0].string
        match_score =  dom.select(".vs-score span")
        if len(match_score) == 0:
            left_score = right_score = 0
        else:
            left_score  = match_score[0].string
            right_score = match_score[1].string
        t_rate_list =  dom.select(".tr-hr")
        rate_list = []
        for tr in t_rate_list:
            tds = tr.select("td")
            company_name = tds[1].contents[1]
            win_rate = tds[2].string
            eq_rate = tds[3].string
            fail_rate = tds[4].string
            rate_tr =  {"com_name":company_name,"win":win_rate,"eq":eq_rate,"fail":fail_rate}
            rate_list.append(rate_tr)
        ret = {
            "url":self._url,
            "host_name":host_name,
            "visit_name":visit_name,
            "match_date":match_date,
            "left_score":left_score,
            "right_socre":right_score,
            "match_result": str(left_score) + ":" + str(right_score),
            "rate_list":rate_list
        }
        self.tools.logging(host_name + " VS "+ visit_name + " done")
        return ret