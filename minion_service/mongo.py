# coding:utf-8
from __future__ import absolute_import, unicode_literals
import pymongo
import datetime
from minion_service.util.tools import get_minion_name

__author__ = "golden"
__date__ = '2017/7/21'


class Mongo(pymongo.MongoClient):
    _instance = None

    def __init__(self, config):
        self.config = config
        super(Mongo, self).__init__(host=config.get('mongo.host'), port=config.get('mongo.port'))
        self.db = self.get_database(self.config.get('mongo.db'))
        self.minion_collection = self.db.get_collection('minion')
        self.task_url = self.db.get_collection(self.config.get('mongo.url_collection', 'task_url'))
        self._ip = None
        self.minion = self.minion_collection.find_one({'name': self.config.get('name')})
        self.minion_id = self.minion.get('_id')
        self.minion_name = self.minion.get('name')

    def minion_beat(self):
        if not self.minion_id:
            self.minion_collection.update({'name': self.config.get('name')},
                                          {'$set': {'last_beat': datetime.datetime.utcnow(),
                                                    'ip': self.ip}},
                                          upsert=False)
        else:
            self.minion_collection.update({'_id': self.minion_id},
                                          {'$set': {'last_beat': datetime.datetime.utcnow(),
                                                    'ip': self.ip}},
                                          upsert=False)

    @property
    def ip(self):
        if not self._ip:
            self._ip = get_minion_name(self.config.get('master_url', 'http://localhost:5000'))
        return self._ip

    @property
    def do_job(self):
        minion = self.minion_collection.find_one({'name': self.config.get('name')})
        if minion:
            return minion.get('do_job')
        else:
            return False

    def push(self, url):
        pass

    def pop(self):
        return self.task_url.find_one_and_delete()

    def pop_by_id(self, task_id):
        """
        返回一个url
        :param task_id: 任务的id
        :return:
        """
        return self.task_url.find_one_and_delete({'_id': task_id})

    def get_task(self, task_id):
        pass

    def get_spider(self, task_id):
        spider_id = self.db.get_collection('task').find_one({'_id': task_id}).get('spider')
        return self.db.get_collection(name='spider').find_one({'_id': spider_id})

    def get_project(self, task_id):
        name = self.get_spider(task_id).get('project')
        return self.db.get_collection(name='project').find_one({'_id': name})

    @classmethod
    def __new__(cls, *args, **kwargs):
        """单例模式"""
        if not cls._instance:
            cls._instance = super(Mongo, cls).__new__(*args, **kwargs)
        return cls._instance
