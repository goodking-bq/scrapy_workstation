# coding:utf-8
from __future__ import absolute_import, unicode_literals
from redis import StrictRedis
from scrapy.utils.request import request_fingerprint
import logging
from minion_service.spider_core.mongo import Mongo

__author__ = "golden"
__date__ = '2017/6/6'


class MongoDupeFilter(object):
    def __init__(self, settings, debug=False):
        self.mongo = Mongo.from_settings(settings)
        self.task_id = settings.get('TASK_ID')
        self.logdupes = True
        self.debug = debug
        self.logger = logging.getLogger(__name__)
        self.fingerprint = self.mongo.db.get_collection('fingerprint')

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def request_seen(self, request):
        fp = self.request_fingerprint(request)
        if not self.fingerprint.find_one(
                {'task_id': self.mongo.ObjectId(self.task_id), 'fp': fp}):
            self.fingerprint.insert(
                {'task_id': self.mongo.ObjectId(self.task_id), 'fp': fp})

    def request_fingerprint(self, request):
        return request_fingerprint(request)

    def log(self, request, spider):
        if self.debug:
            msg = "Filtered duplicate request: %(request)s"
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request: %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
            self.logdupes = False
        spider.crawler.stats.inc_value('dupefilter/filtered', spider=spider)

    def clear(self):
        self.fingerprint.remove({'task_id': self.mongo.ObjectId(self.task_id)})
