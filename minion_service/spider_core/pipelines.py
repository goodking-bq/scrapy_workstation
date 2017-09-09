# coding:utf-8
from __future__ import absolute_import, unicode_literals
from .mongo import Mongo

__author__ = "golden"
__date__ = '2017/8/15'


class MongoPipeline(object):
    def open_spider(self, spider):
        self.mongo = Mongo.from_settings(spider.settings)
        self.collection = self.mongo.db.get_collection(spider.settings.get('COLLECTION', spider.name))  # spider 配置存储

    def close_spider(self, spider):
        self.mongo.close()

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
