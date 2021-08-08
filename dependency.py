# -*- coding: utf-8 -*-
# author: Tac
# contact: gzzhanghuaxiong@corp.netease.com

import os

# 依赖库
_DEPENDENCY = [
    'PyQt6',
    'openpyxl',
    'jinja2',
]


def check_dependency():
    for lib_name in _DEPENDENCY:
        try:
            __import__(lib_name)
        except ImportError:
            if os.system('py -3 -m pip install %s' % lib_name):
                from ec_converter import logger
                logger.error('py -3 -m pip install %s FAILED!!!', lib_name)
                logger.log_last_except()
                exit(1)
            __import__(lib_name)
