#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2020-08-29 03:36:13
# Project: zgzcw

from pyspider.libs.base_handler import *
import time


class Handler(BaseHandler):
    crawl_config = {
    }

    def get_time_str(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+8*3600))

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://cp.zgzcw.com/lottery/jchtplayvsForJsp.action?lotteryId=47&type=jcmini&issue=2020-08-27',
                   callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        docs = []
        for e in response.doc('tbody>tr').items():
            score_fields = e.find("td").eq(4).text().split(":")
            doc = {
                "datetime": self.get_time_str(),
                "score": {
                    "host": score_fields[0],
                    "guest": score_fields[1],
                },
                "match": {
                    "id": e.attr.id[3:],
                    "name": e.attr.m,
                    "host-name": e.find("td").eq(3).find("a").text(),
                    "guest-name": e.find("td").eq(5).find("a").text()
                }
            }
            odds = []
            for i in e.find("td").eq(6).find("div").items():
                if len([p for p in i.find("a").items()]) > 1:
                    odds.append({
                        "win": i.find("a").eq(0).text(),
                        "eq": i.find("a").eq(1).text(),
                        "lose": i.find("a").eq(2).text(),
                        "rq": i.find(".rq").text()
                    })
            doc["odds"] = odds
            docs.append(doc)
        return docs
