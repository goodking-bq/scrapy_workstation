# -*- coding: utf-8 -*-
import scrapy
from minion_service.spider_core.spiders import MongoSpider


class DoubanSpider(MongoSpider):
    name = "douban"
    allowed_domains = ["https://movie.douban.com/chart"]
    start_urls = ['http://https://movie.douban.com/chart/']

    def parse(self, response):
        res = response
        print(res)
