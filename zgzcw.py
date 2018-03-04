import di
import tools

class Builder:

    def __init__(self):
        self.tools = tools.Tools()
        self.di = di.Di()
        self.redis = self.di.getRedis()
        self.mongodb = self.di.getMongoDb()

    def run(self):
        for n in range(2201128,2400000):
            url = "http://fenxi.zgzcw.com/"+str(n)+"/bjop"
            self._url = url
            source = self.get_Source(url)
            if source:
                res = self.analysis_html(source)
                self.mongodb["zucai"]["zgzcw"].insert(res)
    
    def get_Source(self,url):
        html = self.redis.get(url)
        if html == None:
            dom = self.tools.get_dom_obj(url)
            if dom:
                self.redis.set(url,dom)
        else:
            dom = self.tools.get_dom_obj_by_content(html)
        if len(dom.select(".error")) == 1:
            self.tools.logging(url+ " get: error")
            return 
        else:
            self.tools.logging(url+ " get: success") 
        return dom

    def analysis_html(self,dom):
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
            rate_list.append({"com_name":company_name,"win":win_rate,"eq":eq_rate,"fail":fail_rate})
        ret = {
            "url":self._url,
            "host_name":host_name,
            "visit_name":visit_name,
            "match_date":match_date,
            "left_score":left_score,
            "right_socre":right_score,
            "rate_list":rate_list
        }
        self.tools.logging(host_name + " VS "+ visit_name + " done")
        return ret