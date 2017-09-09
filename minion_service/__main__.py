# coding:utf-8
from __future__ import absolute_import, unicode_literals
from optparse import OptionParser
from .app import Scrapyd
from .conf import Config
from .log import setup_logger

__author__ = "golden"
__date__ = '2017/7/20'
usage = """
        usage:  %prog  [command] [options]

    Command:
        start       启动
        stop        停止
        restart     重启
        status      状态
        version     版本
        """


def main():
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--daemon", dest='daemon', action="store_true", help="run as daemon")
    parser.add_option("-c", "--config", dest='config', action="store_true", help="config file")
    parser.add_option("-l", "--logfile", dest='logfile', action="store_true", help="log file")
    (options, args) = parser.parse_args()
    config = Config(config_file=options.config)
    setup_logger(config, file_name=options.logfile)
    if len(args) == 0:
        args = ['start']
        options.daemon = True
    if len(args) != 1 or args[0] not in ['start', 'restart', 'status', 'stop', 'version']:
        parser.error('Command Error')
    scrapyd = Scrapyd(config)
    if options.daemon or args[0] != 'start':
        func = getattr(scrapyd, args[0])
        func()
    else:
        scrapyd.daemon = False
        scrapyd.run()
