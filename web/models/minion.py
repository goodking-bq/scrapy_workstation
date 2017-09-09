# coding:utf-8
from __future__ import absolute_import, unicode_literals
from web.extension import db
import datetime

__author__ = "golden"
__date__ = '2017/6/21'

__all__ = ['Minion','MinionLog']


class Minion(db.Document):
    ip = db.StringField(text_help='ip')
    name = db.StringField(text_help='名字')
    create_time = db.DateTimeField(default=datetime.datetime.utcnow)
    do_job = db.BooleanField(default=True)
    running = db.IntField(default=0)
    last_beat = db.DateTimeField()
    meta = {
        'collection': 'minion',
    }


class MinionLog(db.Document):
    """
    Minion 日志
    """
    minion = db.ReferenceField('Minion')
    file_name = db.StringField(required=True)
    level_no = db.IntField(required=True)
    level_name = db.StringField(required=True)
    line_no = db.IntField(required=True)
    log = db.StringField(required=True)
    log_time = db.DateTimeField()
