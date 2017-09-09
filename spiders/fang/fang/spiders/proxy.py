# -*- coding: utf-8 -*-
import scrapy
import urlparse
from scrapy.conf import settings
import copy
from ..items import ProxyItem


class ProxySpider(scrapy.Spider):
    name = "proxy"
    start_urls = ["http://www.66ip.cn/areaindex_%s/1.html" % area for area in range(1, 3)]
    custom_settings = {
        'MONGODB_COLLECTION': 'proxy',
        'ITEM_PIPELINES': {'fang.pipelines.ProxyMongoPipeline': 300},
        'DOWNLOADER_MIDDLEWARES': {
            'fang.middlewares.JavaScriptMiddleware': 543,  # 键为中间件类的路径，值为中间件的顺序
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  # 禁止内置的中间件
        },
        'USE_PROXY': False
    }
    selector_rule = {
        "www.66ip.cn": {
            "settings": {'DOWNLOADER_MIDDLEWARES': {
                'fang.middlewares.JavaScriptMiddleware': 543,  # 键为中间件类的路径，值为中间件的顺序
                'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  # 禁止内置的中间件
            }},
            "start_urls": ["http://www.66ip.cn/areaindex_%s/1.html" % area for area in range(1, 22)],
            "xpath": {
                "all": '//table[@width="100%"]/tbody/tr[position()>1]',
                "ip": './/td[1]/text()',
                "port": './/td[2]/text()',
                "location": './/td[3]/text()',
                "proxy_type": './/td[4]/text()',
            }
        },
        'www.proxy360.cn': {
            "start_urls": ["http://www.proxy360.cn/default.aspx"],
            "xpath": {
                "all": '//div[@class="proxylistitem"]',
                "ip": ".//div/span[1]/text()",
                "port": ".//div/span[2]/text()",
                "location": ".//div/span[4]/text()",
                "proxy_type": ".//div/span[3]/text()"
            }
        },
        'www.kuaidaili.com': {
            "start_urls": ['http://www.kuaidaili.com/proxylist/%s/' % page for page in range(1, 10)],
            "xpath": {
                "all": '//table/tbody/tr',
                "ip": ".//td[1]/text()",
                "port": ".//td[2]/text()",
                "location": ".//td[6]/text()",
                "protocol": ".//td[4]/text()",
                "proxy_type": ".//td[3]/text()"
            }
        }
    }

    def start_requests(self):
        for domain in self.selector_rule:
            # for setting in self.selector_rule[domain]['settings']:
            #     self.settings.set(setting, self.selector_rule[domain]['settings'][setting])
            for url in self.selector_rule[domain]['start_urls']:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # print response.text
        url_parse = urlparse.urlparse(response.url)
        netloc = url_parse.netloc
        xpath = copy.deepcopy(self.selector_rule[netloc]['xpath'])
        items = ProxyItem()
        all = response.xpath(xpath['all'])
        for selector in all:
            items['ip'] = selector.xpath(xpath['ip']).extract_first().strip()
            items['port'] = selector.xpath(xpath['port']).extract_first().strip()
            items['location'] = selector.xpath(xpath['location']).extract_first().strip()
            items['proxy_type'] = selector.xpath(xpath['proxy_type']).extract_first().strip()
            if xpath.has_key('protocol'):
                protocol = selector.xpath(xpath['protocol']).extract_first().strip().lower()
            else:
                protocol = 'http'
            if 'https' in protocol:
                items['is_ssl'] = 1
            else:
                items['is_ssl'] = 0
            items['protocol'] = protocol
            items['location_type'] = 1
            items['checked'] = 0
            yield items
