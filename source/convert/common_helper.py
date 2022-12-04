# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import time
import functools

import genv

FUNC_CALLTIME_THRESHOLD = 2.0  # 认为函数调用时间太长的阈值，单位为秒


def time_it(func):
    """
    在某个函数调用时，记录并打印其调用所用的时间
    Args:
        func: callable
    Returns:
        callable
    """

    @functools.wraps(func)
    def _warpper(*args, **kwargs):
        begin_time = time.time()
        genv.logger.info('[%s]begins......', func.__name__)
        ret = func(*args, **kwargs)
        end_time = time.time()
        delta_time = end_time - begin_time
        if delta_time < FUNC_CALLTIME_THRESHOLD:
            genv.logger.info('[%s]ends (%.2fs)', func.__name__, delta_time)
        else:
            genv.logger.warning('[%s]ends (%.2fs)', func.__name__, delta_time)
        return ret

    return _warpper
