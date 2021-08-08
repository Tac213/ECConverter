# -*- coding: utf-8 -*-
# author: Tac
# contact: gzzhanghuaxiong@corp.netease.com

APP_NAME = 'ECConverter'
APP_ICON = 'res/icon.ico'

LOGGER_NAME = 'ec_converter'
LOG_DIR_NAME = 'log'

PREFERENCE_FILENAME = '.eccpreference'

FORMATTER_FILTER_NAME = 'ecc_formatter'
JINJA_TEMPLATES_DIR_NAME = 'templates'

FUNC_CALLTIME_THRESHOLD = 2.0  # 认为函数调用时间太长的阈值，单位为秒
INT_THRESHOLD = 0.000001  # 认为浮点数是整数的阈值

EXCEL_INFO_SPLITER = ' '  # 所有Excel信息的文件用这个文本来间隔

REF_FILE_SPLITER = ' '  # ref文件用这个文本来间隔
REF_FILE_LINE_FORMAT = '%s %s %s %s %s %s '  # ref文件每一行的格式


class RefInfoIndex(object):
    FROM_EXCEL = 0
    FROM_SHEET = 1
    FIELD_NAME = 2
    FIELD_TYPE = 3
    TO_SHEET = 4
    TO_EXCEL = 5
    LENGTH = 7


class ValidFieldType(object):
    """
    合法的字段类型，经过eval的
    """
    BOOL = bool
    INT = int
    FLOAT = float
    STR = str
    LIST = list
    DICT = dict
    EVAL = 'eval'
    TIME = 'time'
    DATETIME = 'datatime'


class ValidFieldLabel(object):
    OPTIONAL = 'optional'
    REQUIRED = 'required'
    REPEATED = 'repeated'
    M_REPEATED = 'm_repeated'


class TemplateName(object):
    DATA_MODULE = 'data_module.tpl'
    DATA_LIST = 'data_list.tpl'
