# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    publish_date = scrapy.Field()  # 发布时间
    domain = scrapy.Field()
    zone = scrapy.Field()  # 区
    street = scrapy.Field()  # 街道
    community = scrapy.Field()  # 小区
    space = scrapy.Field()  # 面积
    total_price = scrapy.Field()
    m2_price = scrapy.Field()


class ProxyItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()
    location = scrapy.Field()
    location_type = scrapy.Field(default=1)
    proxy_type = scrapy.Field()
    checked = scrapy.Field()  # 检查
    protocol = scrapy.Field()  # 协议
    is_ssl = scrapy.Field()  # https？？
