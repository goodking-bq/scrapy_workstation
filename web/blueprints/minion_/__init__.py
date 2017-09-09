# coding:utf-8
from __future__ import absolute_import, unicode_literals

from flask import Blueprint

from . import pages

__author__ = "golden"
__date__ = '2017/6/21'
bp = Blueprint('minion', __name__, url_prefix='/minion')

bp.add_url_rule('/', view_func=pages.list_minion)
bp.add_url_rule('/list/', view_func=pages.list_minion)
bp.add_url_rule('/log/<string:minion_name>', view_func=pages.minion_log)
bp.add_url_rule('/heart_beat/', view_func=pages.heart_beat)
