# coding:utf-8
from __future__ import absolute_import, unicode_literals
import requests
import socket

__author__ = "golden"
__date__ = '2017/5/27'


def get_minion_name(master_url):
    url = '%s/minion/heart_beat/' % (master_url)
    try:
        res = requests.get(url).json()
        return res.get('minion_ip')
    except Exception as e:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
