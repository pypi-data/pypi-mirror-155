#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'YAnho.wen'
__mtime__ = '2021/12/21'

"""
import os
import datetime
import random
import hashlib

from clife_svc.libs.context import request_id

PREFIX = "CLIFE_"


def console_log_filter(record) -> bool:
    record['req_id'] = request_id.get()
    return True


def svc_log_filter(record) -> bool:
    if record['name'] in ['clife_svc.disconf', 'clife_svc.configmap']:
        return False
    return True


def format_multi_value(context: str):
    """
    对多值内容进行字典转换
    """
    value_dict = {}
    lines = [_ for _ in context.replace('↵', '\n').splitlines() if not _.strip().startswith('#')]
    for line in lines:
        contents = line.replace(" ", "").split('=')
        if len(contents) == 2:
            value_dict[contents[0]] = contents[1]
    return value_dict


def get_env(name):
    """
    从环境变量中获取key对应的value
    """
    for env_key in [name, name.upper(),
                    "_".join([_ for _ in name.split('.')]),
                    "_".join([_.upper() for _ in name.split('.')])]:
        for key in [env_key, PREFIX + env_key]:
            value = os.environ.get(key)
            if value is not None:
                return value


def get_md5(string):
    hl = hashlib.md5()
    hl.update(string.encode(encoding='utf-8'))
    return hl.hexdigest()


def _tid_maker_1():
    return '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now())


def _tid_maker_2():
    return '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()) + ''.join(
        [str(random.randint(0, 9)) for _ in range(5)])


def tid_maker():
    return _tid_maker_2()
