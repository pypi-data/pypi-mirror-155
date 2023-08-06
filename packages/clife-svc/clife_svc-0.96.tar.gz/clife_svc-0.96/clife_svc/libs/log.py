#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'andy.hu'
__mtime__ = '2021/07/09'

"""
import os
import sys

from loguru import logger as klogger

from clife_svc.libs.log_formatter import formatter
from clife_svc.libs.utils import console_log_filter, svc_log_filter

klogger.remove(handler_id=None)
klogger.add(sys.stderr, filter=console_log_filter, format=formatter.format)


def init_conf_log(log_path: str):
    """
    初始化disconf日志模块
    :param log_path: 日志输出路径
    :return:
    """
    klogger.add(os.path.join(log_path, 'disconf.log'), format=formatter.format, filter='clife_svc.disconf')
    klogger.add(os.path.join(log_path, 'configmap.log'), format=formatter.format, filter='clife_svc.configmap')


def init_svc_log(log_path: str, log_level='INFO'):
    """
    初始化服务日志模块
    :param log_path: 日志输出路径
    :param log_level: 日志级别，从低到高依次为 TRACE|DEBUG|INFO|SUCCESS|WARNING|ERROR|CRITICAL
    :return:
    """
    klogger.add(
        os.path.join(log_path, '{time:YYYY-MM-DD}.log'),
        format=formatter.format,
        level=log_level,
        enqueue=True,
        rotation='00:00',
        retention='10 days',
        encoding='utf-8',
        compression='zip',
        filter=svc_log_filter,
    )


if __name__ == '__main__':
    print(os.path.dirname(__file__))
    print(os.path.dirname(os.path.dirname(__file__)))
    print(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    print(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
