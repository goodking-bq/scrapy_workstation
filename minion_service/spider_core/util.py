# coding:utf-8
from __future__ import absolute_import, unicode_literals
from scrapy.utils.misc import load_object as load_object_

__author__ = "golden"
__date__ = '2017/6/7'


def load_object(path):
    if not hasattr(path, '__call__'):  # 如果是给str
        return load_object_(path)
    else:  # 给class
        return path
