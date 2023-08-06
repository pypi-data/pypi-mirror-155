#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'YAnho.wen'
__mtime__ = '2021/12/23'

"""


class Formatter:

    def __init__(self):
        self.fmt = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | " \
                   "<level>{level: <8}</level> | " \
                   "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | " \
                   "<level>{message}</level>\n{exception}"
        self.req_fmt = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | " \
                       "<level>{level: <8}</level> | " \
                       "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | " \
                       "<cyan>{req_id}</cyan> | " \
                       "<level>{message}</level>\n{exception}"

    def format(self, record):
        if not record['req_id']:
            return self.fmt
        return self.req_fmt


formatter = Formatter()
