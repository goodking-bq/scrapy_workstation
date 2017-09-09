# coding:utf-8
from __future__ import absolute_import, unicode_literals
import sys
import re
from minion_service.__main__ import main

__author__ = "golden"
__date__ = '2017/5/26'

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.argv.append('start')
    # sys.argv.append('-d')
    sys.exit(main())
