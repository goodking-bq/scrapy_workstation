# coding:utf-8
from __future__ import absolute_import, unicode_literals

from flask import Blueprint

from . import pages

__author__ = "golden"
__date__ = '2017/6/21'

bp = Blueprint('home', __name__, url_prefix='/')
bp.add_url_rule('index/', view_func=pages.index)
bp.add_url_rule('/', view_func=pages.index)
bp.add_url_rule('proxy______', view_func=pages.proxy)
bp.add_url_rule('day_new/', view_func=pages.day_new)
bp.add_url_rule('day_average_price/', view_func=pages.day_average_price)

