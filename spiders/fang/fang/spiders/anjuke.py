# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import scrapy
from ..items import FangItem
import datetime
import sys
from scrapy_webdriver.http import WebdriverRequest


class AnjukeSpider(scrapy.Spider):
    name = "anjuke"
    start_urls = ['http://chengdu.anjuke.com/sale/o5/']
    custom_settings = {
        'MONGODB_COLLECTION': 'anjuke',
        'SPIDER_MIDDLEWARES': {
            'scrapy_webdriver.middlewares.WebdriverSpiderMiddleware': 543,
        },

        'DOWNLOAD_HANDLERS': {
            'http': 'scrapy_webdriver.download.WebdriverDownloadHandler',
            'https': 'scrapy_webdriver.download.WebdriverDownloadHandler',
        },
        'USE_PROXY': True,
        # 'USER_AGENT': 'Baiduspider+(+http://www.baidu.com/search/spider.htm)'
    }

    def start_requests(self):
        for url in self.start_urls:
            yield WebdriverRequest(url=url, callback=self.list_page)

    def list_page(self, response):
        urls = response.xpath('//div[@class="house-title"]/a/@href').extract()
        for url in urls:
            yield WebdriverRequest(url, callback=self.parse)
        next_page = response.xpath('//a[@class="aNxt"]/@href').extract_first()
        if next_page:
            yield WebdriverRequest(next_page, callback=self.list_page)

    def parse(self, response):
        encoding = sys.stdout.encoding or 'utf-8'
        item = FangItem()
        item['title'] = response.css('.long-title::text').extract_first().strip()
        item['url'] = response.url
        publish_date = response.css('.houseInfo-title span::text').extract_first().split(u'：')[-1]
        item['publish_date'] = str(datetime.datetime.strptime(publish_date.encode(encoding),
                                                              u"%Y年%m月%d日".encode(encoding)).date())
        item['domain'] = 'anjuke'
        item['community'] = response.css('.loc-text a::text').extract()[1]
        area = response.css('.loc-text a::text').extract_first().strip()
        if area and not area.endswith('区'):
            area += '区'
        item['zone'] = area
        item['street'] = response.css('.loc-text ::text').extract()[3].splitlines()[1].strip()
        item['total_price'] = int(round(float(response.css('.light em::text').extract_first())))
        item['m2_price'] = int(response.css('.third-col dl')[1].css('dd ::text').extract_first().split(' ')[0])
        yield item
