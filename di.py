#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pymongo import MongoClient
import redis

# 依赖注入
class Di:

    def __init__(self):
        Di.mongodb = None
        Di.redis = None

    # mongodb client 
    def getMongoDb(self):
        if Di.mongodb == None:
            Di.mongodb =  MongoClient('127.0.0.1', 27017)
        return Di.mongodb
    
    def getRedis(self):
        if Di.redis == None:
            Di.redis = redis.Redis('127.0.0.1', 6379)
        return Di.redis