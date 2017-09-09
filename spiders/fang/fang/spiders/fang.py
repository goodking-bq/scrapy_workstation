# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import scrapy
from ..items import FangItem


class FangSapider(scrapy.Spider):
    name = 'fang'
    start_urls = ['http://esf.cd.fang.com/house/h316/']
    custom_settings = {
        'MONGODB_COLLECTION': 'fang',
        'DOWNLOAD_DELAY': 0,
        # 'USER_AGENT': 'Baiduspider+(+http://www.baidu.com/search/spider.htm)'
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.list_page)

    def list_page(self, response):
        for detail_url in response.xpath("//div[@class='houseList']//dl//p[@class='title']//a/@href").extract():
            url = response.urljoin(detail_url)
            yield scrapy.Request(url=url, callback=self.parse)
        next_page = response.urljoin(
            response.xpath("//div[@name='div_PageList']/a[@id='PageControl1_hlk_next']/@href").extract_first())
        yield scrapy.Request(url=next_page, callback=self.list_page)

    def parse(self, response):
        items = FangItem()
        mainbox = response.css('.wid1200')
        house_info = mainbox.css('.trl-item1')
        _area = house_info[1].css('.tt::text').extract_first()[:-2]
        m2_price = house_info[2].css('.tt::text').extract_first()[:-4]
        items['title'] = mainbox.css('.title::text').extract_first().strip()
        items['url'] = response.url
        items['publish_date'] = mainbox.css('.content-item')[0].css('.text-item')[-1].css(
            '.rcont::text').extract_first()[:10].strip()
        items['domain'] = 'fang'
        items['community'] = mainbox.css('.trl-item2')[-2].css('.blue::text').extract_first().strip()
        area = mainbox.css('.trl-item2')[-1].css('.blue::text').extract()[0].strip()
        if area and not area.endswith('区'):
            area += '区'
        items['zone'] = area
        items['street'] = mainbox.css('.trl-item2')[-1].css('.blue::text').extract()[1].strip()
        items['total_price'] = int(round(float((mainbox.css('.sty1 i::text').extract_first()))))
        items['m2_price'] = int(m2_price)
        items['space'] = _area
        yield items
