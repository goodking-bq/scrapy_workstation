# coding:utf-8
from __future__ import absolute_import, unicode_literals
import scrapy
from .mongo import Mongo
import logging
from .log import LogMongoHandler
import datetime

__author__ = "golden"
__date__ = '2017/6/5'


class MongoSpiderMixin(object):
    start_urls_key = None
    make_start_urls_size = None
    task_id = None

    def setup_mongo(self, crawler=None):
        self.setup_logger(crawler)
        self.task_id = crawler.settings.get('TASK_ID')
        if not hasattr(self, 'mongo'):
            if crawler is None:
                crawler = getattr(self, 'crawler', None)
            if not crawler:
                raise Exception('crawler must give')
            settings = crawler.settings
            self.mongo = Mongo.from_settings(settings)
        if self.make_start_urls_size is None:
            self.make_start_urls_size = crawler.settings.getint('MAKE_START_URLS_SIZE', crawler.settings.getint(
                'CONCURRENT_REQUESTS'))  # 每次最多读多少个
        return self

    def start_requests(self):
        """
        
        :return: 
        """
        return self.next_requests()

    def next_requests(self):
        total = 0
        while total < self.make_start_urls_size:
            url = self.mongo.db.task_url.find_one_and_delete({'task_id': self.mongo.ObjectId(self.task_id)})
            if not url:
                break

            req = self.make_requests_from_url(url['url'])
            if req:
                total += 1
                yield req
            else:
                self.log("Request not made from data: %r" % url['url'], logging.WARNING)

    def log(self, message, level=logging.DEBUG, **kw):
        """Log the given message at the given log level

        This helper wraps a log call to the logger within the spider, but you
        can use it directly (e.g. Spider.logger.info('msg')) or use any other
        Python logger too.
        """
        self.logger.log(level, message, **kw)

    def setup_logger(self, crawler=None):
        # logging.basicConfig()
        if crawler is None:
            crawler = getattr(self, 'crawler', None)
        if not crawler:
            raise Exception('crawler must give')
        logger = logging.getLogger()
        mongo_log = LogMongoHandler.from_settings(crawler.settings)
        logger.addHandler(mongo_log)


class MongoSpider(MongoSpiderMixin, scrapy.Spider):
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(MongoSpider, cls).from_crawler(crawler)
        spider = spider.setup_mongo(spider)
        spider.mongo.spider_start()
        return spider

    @staticmethod
    def close(spider, reason):
        spider.mongo.spider_close()
        return scrapy.Spider.close(spider, reason)
