# coding:utf-8
from __future__ import absolute_import, unicode_literals
from web.models import Minion, MinionLog
from flask import render_template, url_for, redirect, request

__author__ = "golden"
__date__ = '2017/6/21'


def list_minion():
    minions = Minion.objects.all()
    return render_template('minion/list.html', minions=minions)


def heart_beat():
    return request.remote_addr


def minion_log(minion_name):
    """日志"""
    limit = request.args.get('limit') or 20
    minion = Minion.objects(name=minion_name).first()
    logs = MinionLog.objects(minion=minion).order_by('-log_time').limit(int(limit))
    logs = reversed(logs)
    return render_template('minion/log.html', logs=logs)
