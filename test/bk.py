# coding:utf-8
from __future__ import absolute_import, unicode_literals
import subprocess

__author__ = "golden"
__date__ = '2017/7/22'

p = subprocess.Popen('ls', shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
p.stdin.write(b'\n\n\n\n\n\n\naaa\n')
print(p.wait())
print(p.stdout.read())
print(p.stderr.read())
