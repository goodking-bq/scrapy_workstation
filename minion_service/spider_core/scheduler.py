# coding:utf-8
from __future__ import absolute_import, unicode_literals
from scrapy.utils.misc import load_object
from scrapy.utils.reqser import request_from_dict, request_to_dict
import json
from .mongo import Mongo

__author__ = "golden"
__date__ = '2017/6/6'


class MongoScheduler(object):
    def __init__(self, dupefilter, stats=None, crawler=None):
        self.mongo = Mongo.from_settings(crawler.settings)
        self.df = dupefilter
        self.stats = stats
        self.task_id = crawler.settings.get('TASK_ID')

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        dupefilter_cls = load_object(settings['DUPEFILTER_CLASS'])
        dupefilter = dupefilter_cls.from_settings(settings)
        return cls(dupefilter, stats=crawler.stats, crawler=crawler)

    def open(self, spider):
        self.spider = spider
        self.schedule = self.mongo.db.get_collection('schedule')

    def enqueue_request(self, request):
        """入队列"""
        if not request.dont_filter and self.df.request_seen(request):
            self.df.log(request, self.spider)
            return False
        if self.stats:
            self.stats.inc_value('scheduler/enqueued/redis', spider=self.spider)
        self.schedule.insert({'task_id': self.mongo.ObjectId(self.task_id),
                              'encode_request': self._encode_request(request)})

    def next_request(self):
        encoded_request = self.schedule.find_one_and_delete(
            {'task_id': self.mongo.ObjectId(self.task_id)})
        if encoded_request:
            request = self._decode_request(encoded_request['encode_request'])
            if request and self.stats:
                self.stats.inc_value('scheduler/dequeued/redis', spider=self.spider)
            return request

    def __len__(self):
        return self.mongo.db.schedule.find({'task_id': self.mongo.ObjectId(self.task_id)}).count()

    def has_pending_requests(self):
        return len(self) > 0

    def close(self, reason):
        self.clear()
        self.df.clear()

    def clear(self):
        self.schedule.remove({'task_id': self.mongo.ObjectId(self.task_id)})

    def _encode_request(self, request):
        obj = request_to_dict(request, self.spider)
        return json.dumps(obj)

    def _decode_request(self, encoded_request):
        obj = json.loads(encoded_request)
        return request_from_dict(obj, self.spider)
