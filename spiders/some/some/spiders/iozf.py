# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import scrapy
from ..items import FileItem


class IozfSpider(scrapy.Spider):
    name = 'iozf'
    start_urls = ['http://1024.91lulea.blue/pw/thread.php?fid=5']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.list_page)

    def list_page(self, response):
        all_a = response.xpath('//tbody[@style="table-layout:fixed;"]/tr//a')
        for a in all_a:
            a_font = a.xpath('./font')
            url = a.xpath('./@href').extract_first()
            if not a_font and 'php' not in url:
                url = response.urljoin(url=url)
                yield scrapy.Request(url=url, callback=self.detail_page)

    def detail_page(self, response):
        url = response.xpath('//tr[@class="tr1"]//div[@class="tpc_content"]/a/@href').extract_first()
        yield scrapy.Request(url, callback=self.post_page)

    def post_page(self, response):
        form = response.xpath('//form')
        url = form.xpath('./@action').extract_first()
        _type = form.xpath('./input[@name="type"]/@value').extract_first()
        _id = form.xpath('./input[@name="id"]/@value').extract_first()
        _name = form.xpath('./input[@name="name"]/@value').extract_first()
        url = response.urljoin(url)
        yield scrapy.FormRequest(url=url, callback=self.parse, formdata=dict(type=_type, id=_id, name=_name))

    def parse(self, response):
        item = FileItem()
        item['name'] = 'a.torrent'
        item['body'] = response.body
        yield item
