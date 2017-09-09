# -*- coding: utf-8 -*-
from minion_service.spider_core.spiders import MongoSpider
import scrapy
from ..items import QiubaiItem


class QiubaiSpider(MongoSpider):
    name = 'qiubai'
    allowed_domains = ['www.qiushibaike.com']
    start_urls = ['http://www.qiushibaike.com/']

    custom_settings = {
        'USER_AGENT': "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.0 Chrome/39.0.2146.0 Safari/537.36"
    }

    def parse(self, response):
        item = QiubaiItem()
        item['url'] = response.url
        contents = response.css('.content span::text').extract()
        next_page = response.css('.pagination a::attr(href)').extract()[-1]
        page = int(next_page.split('/')[-2])
        if page < 10:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)
        for content in contents:
            item['content'] = content.strip()
            yield item
