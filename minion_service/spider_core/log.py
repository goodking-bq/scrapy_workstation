# coding:utf-8
from __future__ import absolute_import, unicode_literals
import logging
import datetime
from .mongo import Mongo

__author__ = "golden"
__date__ = '2017/8/15'


class LogMongoHandler(logging.Handler):
    """
    将日志记录在mongodb里
    """

    def __init__(self, task_id, mongo):
        super(LogMongoHandler, self).__init__()
        self.task_id = task_id
        self.mongo = mongo
        self.log_collection = self.mongo.db.get_collection('task_log')

    @classmethod
    def from_settings(cls, settings):
        task_id = settings.get('TASK_ID')
        mongo = Mongo.from_settings(settings)
        return cls(task_id, mongo)

    def emit(self, record):
        file_name = record.filename
        level_name = record.levelname
        level_no = record.levelno
        log = record.message
        line_no = record.lineno
        log_time = datetime.datetime.utcnow()
        try:
            self.log_collection.insert({
                'task': self.mongo.ObjectId(self.task_id),
                'file_name': file_name,
                'level_name': level_name,
                'level_no': level_no,
                'log': log,
                'line_no': line_no,
                'log_time': log_time,
                'minion': self.mongo.minion_id
            })
        except Exception as e:
            print('error.............................')
