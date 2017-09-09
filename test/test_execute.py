# coding:utf-8
from __future__ import absolute_import, unicode_literals
from multiprocessing import Process
from minion_service.redis_cli import Redis
from minion_service.conf import config
import os
from minion_service.util.runner import run_spider, list_spider
import base64

project = 'fang'

redis = Redis(config)


def egg_to_redis():
    egg_file = os.path.join(config.base_dir, '../eggs/1495421780.egg')
    temp_file = os.path.join(config.base_dir, '../eggs/ttt.egg')
    redis.hset('SCRAPYD:PROJECTS', 'fang', base64.encodestring(open(egg_file, 'rb').read()))
    f = open(temp_file, 'wb')
    f.write(base64.decodestring(redis.get('egg_temp')))
    f.close()


if __name__ == '__main__':
    from minion_service.main_process import Scrapyd

    A = Scrapyd()
    A.run()
