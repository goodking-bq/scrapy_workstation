# -*- coding: utf-8 -*-
from __future__ import unicode_literals


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DongmanPipeline(object):
    def open_spider(self, spider):
        self.btdongman = open('result/btdongman.txt', 'wb')
        self.btyazhou = open('result/btyazhou.txt', 'wb')
        self.btoumei = open('result/btoumei.txt', 'wb')
        self.xunleichangpian = open('result/xunleichangpian.txt', 'wb')

    def close_spider(self, spider):
        self.btdongman.close()
        self.btyazhou.close()
        self.btoumei.close()
        self.xunleichangpian.close()

    def process_item(self, item, spider):
        line = item['title'] + '   ' + item['link'] + '\n'
        if 'btdongman' in item['link']:
            self.btdongman.write(line.encode('utf-8'))
        elif 'btyazhou' in item['link']:
            self.btyazhou.write(line.encode('utf-8'))
        elif 'btoumei' in item['link']:
            self.btoumei.write(line.encode('utf-8'))
        elif 'xunleichangpian' in item['link']:
            self.xunleichangpian.write(line.encode('utf-8'))
        return item


class BtPineLine(object):
    def process_item(self, item, spider):
        import time
        name = 'bt/' + str(time.time())
        with file(name, 'w') as f:
            f.write(item['body'])
        return item
