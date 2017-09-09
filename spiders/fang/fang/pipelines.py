# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class FangPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def open_spider(self, spider):
        self.connection = MongoClient(
            spider.settings['MONGODB_SERVER'],
            spider.settings['MONGODB_PORT']
        )
        db = self.connection[spider.settings['MONGODB_DB']]
        self.collection = db[spider.settings['MONGODB_COLLECTION']]

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.collection.update({"url": item['url']}, {"$set": dict(item)},
                               upsert=True)
        return item


class ProxyMongoPipeline(object):
    def open_spider(self, spider):
        self.connection = MongoClient(
            spider.settings['MONGODB_SERVER'],
            spider.settings['MONGODB_PORT']
        )
        db = self.connection[spider.settings['MONGODB_DB']]
        coll = spider.settings['MONGODB_COLLECTION']
        self.collection = db[coll]

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.collection.update({"ip": item['ip']}, {"$set": dict(item)},
                               upsert=True)
        return item
