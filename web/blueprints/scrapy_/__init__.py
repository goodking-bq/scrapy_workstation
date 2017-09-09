# coding:utf-8
from __future__ import absolute_import, unicode_literals

from flask import Blueprint

from . import pages

__author__ = "golden"
__date__ = '2017/6/22'

bp = Blueprint('scrapy', __name__, url_prefix='/scrapy')

bp.add_url_rule('/project/', view_func=pages.project)
bp.add_url_rule('/refresh_project/', view_func=pages.refresh_project)
bp.add_url_rule('/spider/', view_func=pages.spider)
bp.add_url_rule('/add_start_url/', view_func=pages.add_start_url, methods=['POST'])
bp.add_url_rule('/push_start_url/', view_func=pages.push_start_url)
bp.add_url_rule('/tasks/', view_func=pages.tasks)
bp.add_url_rule('/spider_logs/', view_func=pages.spider_logs)
bp.add_url_rule('/project_manager/', view_func=pages.project_manager, methods=['POST'])
