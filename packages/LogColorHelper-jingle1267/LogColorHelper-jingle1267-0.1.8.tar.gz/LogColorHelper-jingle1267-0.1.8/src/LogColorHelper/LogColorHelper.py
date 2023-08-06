# !/usr/bin/python
# -*- coding:utf-8 -*-
"""
@Author  : jingle1267
@Time    : 2020-12-18 01:08
@desc：  : 建议日志颜色控制
"""

LOG_COLOR_YELLOW = '\033[1;33m{0}\033[0m'

LOG_COLOR_GREEN = '\033[1;32m{0}\033[0m'

LOG_COLOR_RED = '\033[1;31m{0}\033[0m'


def yellow(log):
    print(LOG_COLOR_YELLOW.format(log))


def green(log):
    print(LOG_COLOR_GREEN.format(log))


def red(log):
    print(LOG_COLOR_RED.format(log))


def p(log):
    print(log)


if __name__ == '__main__':
    print(LOG_COLOR_YELLOW.format('yellow log'))
    print(LOG_COLOR_GREEN.format('green log'))
    print(LOG_COLOR_RED.format('red log'))
    p('normal log')
