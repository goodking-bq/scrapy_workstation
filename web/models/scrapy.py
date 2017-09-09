# coding:utf-8
from __future__ import absolute_import, unicode_literals
from web.extension import db
import datetime

__author__ = "golden"
__date__ = '2017/6/21'

__all__ = ['Project', 'Spider', 'Task', 'TaskSchedule', 'TaskUrl','TaskLog']


class Project(db.Document):
    name = db.StringField(required=True)
    alias = db.StringField(required=True)  # 别名
    spiders = db.ListField(db.ReferenceField('Spider'))
    description = db.StringField()  # 说明
    egg = db.StringField()  # egg
    last_beat = db.DateTimeField()
    create_time = db.DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        "indexes": [
            {
                "fields": {"name"},
                "unique": True
            }
        ]
    }


class Spider(db.Document):
    name = db.StringField(required=True)
    project = db.ReferenceField('Project')  # 项目
    start_urls = db.ListField(db.URLField())  # 开始url
    create_time = db.DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'collection': 'spider',
        'indexes': [
            {'fields': ('name', 'project'), 'unique': True}
        ]
    }

    def __repr__(self):
        return self.name

    __str__ = __repr__

    def start_urls_key(self):
        return '%s:%s:%s:START_URLS' % (self._redis.prefix_key, self.project.name, self.name)


class Task(db.Document):
    """任务队列"""
    spider = db.ReferenceField('Spider')  # 所属ID
    start_urls = db.ListField(db.URLField())  #
    start_time = db.DateTimeField(default=datetime.datetime.utcnow)
    stop_time = db.DateTimeField()
    elapsed = db.FloatField()


class TaskUrl(db.Document):
    task_id = db.ObjectIdField()
    url = db.URLField()
    meta = {
        'collection': 'task_url',
    }


class TaskLog(db.Document):
    """任务日志"""
    minion = db.ReferenceField('Minion')
    task = db.ReferenceField('Task')
    file_name = db.StringField(required=True)
    level_no = db.IntField(required=True)
    level_name = db.StringField(required=True)
    line_no = db.IntField(required=True)
    log = db.StringField(required=True)
    log_time = db.DateTimeField()


class TaskSchedule(db.Document):
    """Schedule 队列"""
    task_id = db.ObjectIdField()
    request = db.StringField()
    is_active = db.BooleanField()
    create_time = db.DateTimeField(default=datetime.datetime.utcnow)
    update_time = db.DateTimeField()

    meta = {
        'collection': 'task_schedule',
        'indexes': [{'fields': ['task_id']}]
    }
