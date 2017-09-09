# coding:utf-8
from __future__ import absolute_import, unicode_literals
from gevent.server import StreamServer

__author__ = "golden"
__date__ = '2017/5/27'


def handle(sock, address):
    print('新的客户端: %s:%s' % address)
    print('data:%s' % sock.recv(1024))
    sock.send(b"Hello from a telnet!\n")


if __name__ == '__main__':
    server = StreamServer(('0.0.0.0', 8883), handle)
    server.serve_forever()
