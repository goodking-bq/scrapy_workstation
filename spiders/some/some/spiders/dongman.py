# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import scrapy
from ..items import DongmanItem


class DongmanSapider(scrapy.Spider):
    name = 'dongman'
    start_urls = ['http://1122ya.com/xiazaiqu/btdongman', 'http://1122ya.com/xiazaiqu/xunleichangpian',
                  'http://1122ya.com/xiazaiqu/btyazhou', 'http://1122ya.com/xiazaiqu/btoumei']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers={
                'User-Agent': "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.0 Chrome/39.0.2146.0 Safari/537.36"})

    def parse(self, response):
        items = DongmanItem()
        for a in response.xpath("//ul[@class='news_list']//a"):
            items['title'] = a.xpath('text()').extract_first()
            items['link'] = 'http://1122ya.com' + a.xpath('@href').extract_first()
            yield items
        next_page = response.xpath("//div[@class='page']//a")[-2]
        if next_page.xpath('text()').extract_first() == '下一页':
            url = 'http://1122ya.com/' + next_page.xpath('@href').extract_first()
            yield scrapy.Request(url=url, callback=self.parse, headers={
                'User-Agent': "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.0 Chrome/39.0.2146.0 Safari/537.36"})
