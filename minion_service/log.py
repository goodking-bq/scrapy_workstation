# coding:utf-8
from __future__ import absolute_import, unicode_literals
import logging
import datetime

__author__ = "golden"
__date__ = '2017/5/26'


class LogMongoHandler(logging.Handler):
    """
    将日志记录在mongodb里
    """

    def __init__(self, config):
        super(LogMongoHandler, self).__init__()
        self.config = config
        if not hasattr(self, 'mongo'):
            self.setup_mongo()

    def setup_mongo(self):
        from .mongo import Mongo
        self.mongo = Mongo(self.config)
        self.collection = self.mongo.db.get_collection('minion_log')

    def emit(self, record):
        file_name = record.filename
        level_name = record.levelname
        level_no = record.levelno
        log = record.message
        line_no = record.lineno
        log_time = datetime.datetime.utcnow()
        try:
            self.collection.insert({
                'file_name': file_name,
                'level_name': level_name,
                'level_no': level_no,
                'log': log,
                'line_no': line_no,
                'log_time': log_time,
                'minion': self.mongo.minion_id
            })
        except:
            print('error.............................')


def setup_logger(config, file_name=None):
    logging.basicConfig()
    logger = logging.getLogger()
    mongo_log = LogMongoHandler(config=config)
    ch = logging.StreamHandler()
    fh = logging.FileHandler(file_name or config.get('log.file'), mode='w')
    level = getattr(logging, config.get('log.level', 'info').upper())
    logger.setLevel(level)
    logformat = config.get('main', {}).get('logformat', '%(asctime)s | %(name)s | %(levelname)s | %(message)s')
    logformat = logging.Formatter(logformat)
    mongo_log.setFormatter(logformat)
    ch.setFormatter(logformat)
    fh.setFormatter(logformat)
    logger.addHandler(mongo_log)
    logger.addHandler(ch)
    logger.addHandler(fh)
