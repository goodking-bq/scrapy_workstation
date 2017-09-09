# coding:utf-8
from __future__ import absolute_import, unicode_literals
from optparse import OptionParser
import multiprocessing
from minion_service.mongo import Mongo
from .util import Daemon, get_minion_name, run_spider
import time
import logging

__author__ = "golden"
__date__ = '2017/7/20'

logger = logging.getLogger(__name__)


class Scrapyd(Daemon):
    """
    主进程，负责定时同步任务，动态创建spider 子进程，心跳等
    """

    def __init__(self, config):
        self.config = config
        self.mongo = Mongo(self.config)
        self.subprocess = {}
        self.running = True
        self.daemon = True
        self.minion_name = self.config.get('name') or get_minion_name(self.config)
        self.minion_id = str(self.mongo.db.minion.find_one({'name': self.minion_name})['_id'])
        super(Scrapyd, self).__init__(pidfile=self.config.get('pid_file', '/var/run/scrapyd.pid'))

    def run(self):
        logger.debug('主进程开始运行。。。')
        try:
            while self.running:
                self.mongo.minion_beat()
                self._run_spider()
                self.check_subprocess()
                time.sleep(1)
                logger.debug('主进程运行中。。。')
        except Exception as e:
            logger.error(e.__str__())

    def _run_spider(self):
        for url in self.mongo.task_url.find():  # 有start_urls,并且spider没启动，则启动spider
            task_id = url.get('task_id')  # objectid
            if str(task_id) not in self.subprocess.keys():
                project = self.mongo.get_project(task_id)
                spider = self.mongo.get_spider(task_id)
                _spider = multiprocessing.Process(target=run_spider, name=str(task_id), args=(
                    project.get('egg'), project['name'], spider['name'], task_id, self.minion_id))
                _spider.daemon = True
                self.subprocess[str(task_id)] = _spider
                _spider.start()
                if self.daemon:
                    self.append_pid(_spider.pid)
                logger.debug('%s 运行开始运行,PID: %s' % (str(task_id), _spider.pid))
            else:
                logger.debug('%s 运行中,PID: %s' % (str(task_id), self.subprocess[str(task_id)].pid))

    def restart(self):
        logger.debug('主进程开始运行。。。')
        return super(Scrapyd, self).restart()

    def start(self):
        logger.debug('主进程开始运行。。。')
        return super(Scrapyd, self).start()

    def stop(self):
        msg = ''
        for pid in self.subprocess_pids:
            logger.warning('正在停止 %s' % pid)
            msg += self.kill_pid(int(pid)) + '\n'
        msg += super(Scrapyd, self).stop()
        return msg

    def check_subprocess(self, pro=None):
        if not pro:
            _dead = []
            for pro in self.subprocess:
                if self.subprocess[pro].is_alive():
                    logger.debug('%s 运行中。。。' % pro)
                    if self.daemon:
                        self.append_pid(self.subprocess[pro].pid)
                else:
                    _dead.append(pro)
                    if self.daemon:
                        self.remove_pid(self.subprocess[pro].pid)
                    logger.debug('%s 已停止' % pro)
            for _d in _dead:
                self.subprocess.pop(_d)
        else:
            pass
