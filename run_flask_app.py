# coding:utf-8
from __future__ import absolute_import, unicode_literals
import os

__author__ = "golden"
__date__ = '2017/1/18'

from web.app import create_app

app = create_app(os.environ.get('APP_CONFIG', 'web_config.Developer'))
if __name__ == '__main__':
    app.run(port=5103, debug=True, host='0.0.0.0')
