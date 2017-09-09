# coding:utf-8
from __future__ import absolute_import, unicode_literals
from multiprocessing import JoinableQueue, Process, freeze_support
import time

__author__ = "golden"
__date__ = '2017/5/26'

import multiprocessing, sys, time


def main_loop(l):
    time.sleep(4)
    l.acquire()

    # raise an EOFError, I don't know why .
    # _input = input('What kind of food do you like?')

    print(" raw input at 4 sec ")
    l.release()

    return


def test(l):
    i = 0
    while i < 8:
        time.sleep(1)

        l.acquire()
        print('this should run in the background : ', i + 1, 'sec')
        l.release()

        i += 1

    return


if __name__ == '__main__':
    lock = multiprocessing.Lock()

    # try:
    print('hello!')
    mProcess = multiprocessing.Process(target=test, args=(lock,)).start()

    inputProcess = multiprocessing.Process(target=main_loop, args=(lock,)).start()



    # except:
    # sys.exit(0)
