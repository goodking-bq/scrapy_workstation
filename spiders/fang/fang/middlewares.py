# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from scrapy.http import Response, HtmlResponse
import time
import os
import platform
import requests
from scrapy.log import logger
from selenium.webdriver import DesiredCapabilities
import signal
from scrapy.mail import MailSender


class FangSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class JavaScriptMiddleware(object):
    @classmethod
    def process_request(cls, request, spider):
        headers = {'Accept': '*/*',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Cache-Control': 'max-age=0',
                   'User-Agent': spider.settings['USER_AGENT'],
                   'Connection': 'keep-alive',
                   }
        desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        for key, value in headers.iteritems():
            desired_capabilities['phantomjs.page.customHeaders.{}'.format(key)] = value
        desired_capabilities['phantomjs.page.customHeaders.User-Agent'] = spider.settings['USER_AGENT']
        if spider.settings['USE_PROXY']:
            service_args = [
                '--proxy={ip}:{port}'.format(**cls.get_proxy()),
                '--proxy-type=http',
            ]
        else:
            service_args = []
        driver = webdriver.PhantomJS(executable_path=spider.settings['PHANTOMJS_PATH'],
                                     desired_capabilities=desired_capabilities,
                                     service_args=service_args)
        # 隐式等待5秒，可以自己调节
        driver.implicitly_wait(20)
        # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
        # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
        driver.set_page_load_timeout(20)
        # 设置10秒脚本超时时间
        check = True
        driver.set_script_timeout(10)
        driver.get(request.url)
        i = 1
        while not driver.execute_script('return document.readyState') == 'complete' and i < 20:
            logger.warning('sleep 1')
            time.sleep(1)
            i += 1
        js = "var q=document.documentElement.scrollTop=10000"
        driver.execute_script(js)  # 可执行js，模仿用户操作。此处为将页面拉至最底端。
        body = driver.page_source
        logger.warning(u"访问" + request.url)
        url = driver.current_url
        driver.close()
        driver.service.process.send_signal(signal.SIGTERM)
        driver.quit()
        return HtmlResponse(url, body=body, encoding='utf-8', request=request)

    @staticmethod
    def get_proxy():
        url = 'http://192.168.137.3:5100/proxy______'
        res = requests.get(url).json()
        return res

    def process_spider_exception(self, response, exception, spider):
        self._send_mail(subject='')

    def _send_mail(self, subject, body, spider):
        mail_sender = MailSender(smtphost='smtp.mxhichina.com', smtpuser='golden', smtppass='Zz120225883!!')
        mail_sender.send(to=spider.settings['ADMIN_USER'], subject=subject, body=body)
