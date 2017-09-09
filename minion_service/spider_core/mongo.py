# coding:utf-8
from __future__ import absolute_import, unicode_literals
import pymongo
from bson.objectid import ObjectId
import datetime

__author__ = "golden"
__date__ = '2017/7/31'


class Mongo(pymongo.MongoClient):
    _instance = None

    def __init__(self, host, port=27017, db='test', **kwargs):
        super(Mongo, self).__init__(host=host, port=port)
        self.db = self.get_database(db)
        self.ObjectId = ObjectId
        if kwargs.get('minion_id'):
            self.minion_id = self.ObjectId(kwargs.get('minion_id'))
        else:
            self.minion_id = None
        self.task_id = kwargs.get('task_id')

    @classmethod
    def from_settings(cls, settings):
        host = settings.get('MONGO_HOST')
        port = settings.get('MONGO_PORT')
        db = settings.get('MONGO_DB')
        password = settings.get('MONGO_PASSWORD')
        minion_id = settings.get('MINION_ID')
        task_id = settings.get('TASK_ID')
        return cls(host=host, port=port, db=db, password=password, minion_id=minion_id, task_id=task_id)

    @classmethod
    def from_crawl(cls, crawl):
        return cls.from_settings(crawl.settings)

    @classmethod
    def __new__(cls, *args, **kwargs):
        """单例模式"""
        if not cls._instance:
            cls._instance = super(Mongo, cls).__new__(*args, **kwargs)
        return cls._instance

    def spider_start(self):
        self.db.minion.update({'_id': self.minion_id}, {"$inc": {"running": 1}})

    def spider_close(self):
        self.db.minion.update({'_id': self.minion_id}, {"$inc": {"running": -1}})
        if self.task_id:
            self.db.task.update({'_id': self.task_id},
                                {'$set': {'stop_time': datetime.datetime.utcnow()}},
                                upsert=False)
