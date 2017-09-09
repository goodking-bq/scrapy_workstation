# coding:utf-8
from __future__ import absolute_import, unicode_literals
import os, sys

__author__ = "golden"
__date__ = '2017/6/21'


class Base(object):
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SCRAPY_EXE = os.path.join(os.path.dirname(sys.executable), 'scrapy')
    SPIDERDIR = os.path.join(BASEDIR, 'spiders')
    REDIS_URL = 'redis://@{db_host}/2'.format(db_host='192.168.137.3')
    TEMPLATES_AUTO_RELOAD = True
    REDIS_PREFIX = 'SCRAPYD:'
    REDIS_MINION_KEY = REDIS_PREFIX + 'MINION:'
    REDIS_PROJECTS_KEY = REDIS_PREFIX + 'PROJECTS'
    MINION_LOG = 'minion_service.log'
    MASTER_HOST = 'http://192.168.137.1:5001'


class DataBase(object):
    MONGO_HOST = os.environ.get('MONGO_HOST', '192.168.137.1')
    MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'esf')

    MONGODB_HOST = os.environ.get('MONGODB_HOST', '192.168.137.1')
    MONGODB_DB = os.environ.get('MONGODB_DB', 'esf')


class Developer(Base):
    # ==========pymongo============
    MONGO_HOST = os.environ.get('MONGO_HOST', '192.168.137.1')
    MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'esf')

    # ==========mongoengine============
    MONGODB_HOST = os.environ.get('MONGODB_HOST', '192.168.137.1')
    MONGODB_DB = os.environ.get('MONGODB_DB', 'scrapy_workstation')
