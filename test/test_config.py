# coding:utf-8
from __future__ import absolute_import, unicode_literals

__author__ = "golden"
__date__ = '2017/5/27'

from minion_service.conf import Config

config = Config()
print(config.get('redis'))
