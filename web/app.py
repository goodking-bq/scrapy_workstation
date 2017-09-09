# coding:utf-8
from __future__ import absolute_import, unicode_literals
from flask import Flask, Blueprint
import pkgutil, importlib, os
from web.extension import *
import time, datetime

__author__ = "golden"
__date__ = '2017/6/21'


def register_blueprints(app, package_name, package_path):  # 注册蓝图
    """
    自动注册蓝图

    :param app: Flask APP 对象
    :param package_name: 包名
    :param package_path: 包路径
    :return: url 字典
    """
    BAR = []
    for _, name, _ in pkgutil.iter_modules(package_path):
        m = importlib.import_module('%s.%s' % (package_name, name))
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, Blueprint):
                if not app.blueprints.has_key(item.name):  # 加载
                    app.register_blueprint(item)
    return app


def config_template_filter(app):
    @app.template_filter()
    def utc_to_local(utc):
        now_stamp = time.time()
        local_time = datetime.datetime.fromtimestamp(now_stamp)
        utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
        offset = local_time - utc_time
        local_st = utc + offset
        return local_st

    @app.template_filter()
    def timestamp_to_local(timestamp):
        return datetime.datetime.fromtimestamp(float(timestamp))


def create_app(config='config.py'):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    mongo.init_app(app)
    register_blueprints(app, 'web.blueprints', [os.path.join(os.path.dirname(__file__), 'blueprints')])
    config_template_filter(app)
    return app
