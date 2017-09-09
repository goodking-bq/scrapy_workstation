# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import scrapy
from ..items import FangItem
from scrapy_webdriver.http import WebdriverRequest

class LianjiaSpider(scrapy.Spider):
    name = "lianjia"
    start_urls = ['http://cd.lianjia.com/ershoufang/co32/']
    custom_settings = {
        # 'DOWNLOADER_MIDDLEWARES': {
        #     'fang.middlewares.JavaScriptMiddleware': 543,  # 键为中间件类的路径，值为中间件的顺序
        #     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  # 禁止内置的中间件
        # },
        'SPIDER_MIDDLEWARES': {
            'scrapy_webdriver.middlewares.WebdriverSpiderMiddleware': 543,
        },

        'DOWNLOAD_HANDLERS': {
            'http': 'scrapy_webdriver.download.WebdriverDownloadHandler',
            'https': 'scrapy_webdriver.download.WebdriverDownloadHandler',
        },
        'MONGODB_COLLECTION': 'lianjia',
        'USE_PROXY': False,
        'USER_AGENT': 'Baiduspider+(+http://www.baidu.com/search/spider.htm)'
    }

    def start_requests(self):
        for url in self.start_urls:
            yield WebdriverRequest(url=url, callback=self.list_page)

    def list_page(self, response):
        urls = response.xpath('//ul//div[@class="title"]/a/@href').extract()
        for url in urls:
            yield WebdriverRequest(url=response.urljoin(url), callback=self.parse)
        next_page = response.xpath(
            '//div[@class="page-box fr"]//a[@class="on"]/following-sibling::*[1]/@href').extract_first()
        if next_page and int(next_page[14:-5]) < 20:
            yield WebdriverRequest(url=response.urljoin(next_page), callback=self.list_page)

    def parse(self, response):
        item = FangItem()
        item['title'] = response.xpath('//h1[@class="main"]/text()').extract_first()
        item['url'] = response.url
        transaction = response.xpath('//div[@class="transaction"]')
        item['publish_date'] = transaction.xpath('.//li/text()').extract_first()
        item['domain'] = 'lianjia'
        item['community'] = response.xpath('//div[@class="communityName"]//a/text()').extract_first()
        area = response.xpath('//div[@class="areaName"]//a/text()').extract_first().strip()
        if area and not area.endswith('区'):
            area += '区'
        item['zone'] = area
        item['street'] = response.xpath('//div[@class="areaName"]//a/text()').extract()[1].strip()
        item['total_price'] = int(round(float(response.xpath('//span[@class="total"]/text()').extract_first())))
        item['m2_price'] = int(response.xpath('//span[@class="unitPriceValue"]/text()').extract_first())
        yield item
