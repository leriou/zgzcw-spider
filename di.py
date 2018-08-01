#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pymongo import MongoClient

# 依赖注入
class Di:

    def __init__(self):
        Di.mongodb = None

    # mongodb client 
    def getMongoDb(self):
        if Di.mongodb == None:
            Di.mongodb =  MongoClient('127.0.0.1',27017)
        return Di.mongodb






