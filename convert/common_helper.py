# -*- coding: utf-8 -*-
# author: Tac
# contact: gzzhanghuaxiong@corp.netease.com

import time
import functools

import ec_converter
import const


def time_it(func):
    """
    在某个函数调用时，记录并打印其调用所用的时间
    Args:
        func: callable
    Returns:
        None
    """
    @functools.wraps(func)
    def _warpper(*args, **kwargs):
        begin_time = time.time()
        ec_converter.logger.info('[%s]begins......', func.__name__)
        ret = func(*args, **kwargs)
        end_time = time.time()
        delta_time = end_time - begin_time
        if delta_time < const.FUNC_CALLTIME_THRESHOLD:
            ec_converter.logger.info('[%s]ends (%.2fs)', func.__name__, delta_time)
        else:
            ec_converter.logger.warn('[%s]ends (%.2fs)', func.__name__, delta_time)
        return ret

    return _warpper
