# -*- coding: utf-8 -*-
# author: Tac
# contact: gzzhanghuaxiong@corp.netease.com

"""
读取config.json
获取导表的相关配置
未来可能可以通过gui的形式来改config
"""

import os
import json

import ec_converter

# 表所在目录，是个绝对路径，json里填相对路径
EXCEL_DIR = ''
# 导表输出文件目录，是个绝对路径，json里填相对路径
OUTPUT_DIR = ''
# 引用信息文件，是个绝对路径，json里填相对路径
REF_FILENAME = ''
# 所有Excel信息的文件，是个绝对路径，json里填相对路径
EXCEL_INFO_FILENAME = ''
# data list的模块名
DATA_LIST_NAME = ''
# dump文件的拓展名
DUMP_FILE_EXT_NAME = ''
# 缩进字符
INDENT_CHAR = ''
# 引号
QUOTATION_MARKS = ''
# dump的时候是否以tuple的格式dump list
DUMP_LIST_AS_TUPLE = False
# dump的时候是否注释掉ch_name
DUMP_CH_NAME = False
# 引用表的分隔符
REF_SPLITTER = ''
# 默认值的分隔符
DEFAULT_SPLITTER = ''
# 字段名的分隔符
FIELD_NAME_SPLITTER = ''
# repeated值的分隔符
REPEATED_VALUE_SPLITTER = ''
# data名的分隔符
DATA_NAME_SPLITTER = ''
# 字段文本所在的行的索引值
FIELD_TEXT_INDEX = 0
# 字段名所在的行的索引值
FIELD_NAME_INDEX = 0
# 字段类型所在的行的索引值
FIELD_TYPE_INDEX = 0
# 字段label所在的行的索引值
FIELD_LABEL_INDEX = 0
# 字段默认值所在的行的索引值
FIELD_DEFAULT_INDEX = 0
# 数据开始行索引值
ROW_OFFSET = 0
# 数据开始列索引值
COLUMN_OFFSET = 0
# data名字的坐标
DATA_NAME_COORDINATE = [0, 0]
# data名字的后缀
DATA_NAME_SUFFIX = ''
# id的字段名
ID_COLUMN_NAME = ''
# ch_name的字段名
CH_NAME_COLUMN_NAME = ''
# 在拆分工作表时允许重复的字段名
REPEATABLE_FIELD_NAME_IN_SPLITTED_SHEETS = []


def read_config():
    """
    读取config.json，更新全局变量
    Returns:
        None
    """
    global EXCEL_DIR
    global OUTPUT_DIR
    global REF_FILENAME
    global EXCEL_INFO_FILENAME
    global DATA_LIST_NAME
    global DUMP_FILE_EXT_NAME
    global INDENT_CHAR
    global QUOTATION_MARKS
    global DUMP_LIST_AS_TUPLE
    global DUMP_CH_NAME
    global REF_SPLITTER
    global DEFAULT_SPLITTER
    global FIELD_NAME_SPLITTER
    global REPEATED_VALUE_SPLITTER
    global DATA_NAME_SPLITTER
    global FIELD_TEXT_INDEX
    global FIELD_NAME_INDEX
    global FIELD_TYPE_INDEX
    global FIELD_LABEL_INDEX
    global FIELD_DEFAULT_INDEX
    global ROW_OFFSET
    global COLUMN_OFFSET
    global DATA_NAME_COORDINATE
    global DATA_NAME_SUFFIX
    global ID_COLUMN_NAME
    global CH_NAME_COLUMN_NAME
    global REPEATABLE_FIELD_NAME_IN_SPLITTED_SHEETS

    config_json_path = os.path.abspath('settings.json')
    with open(config_json_path, 'r') as f:
        data = json.load(f)

    key = 'excel_dir'
    if key not in data:
        ec_converter.logger.error('\'settings.json\'中的\'%s\'未配置！！请检查！！', key)
    EXCEL_DIR = os.path.abspath(data[key])
    key = 'output_dir'
    if key not in data:
        ec_converter.logger.error('\'settings.json\'中的\'%s\'未配置！！请检查！！', key)
    OUTPUT_DIR = os.path.abspath(data[key])
    key = 'ref_file'
    if key not in data:
        ec_converter.logger.error('\'settings.json\'中的\'%s\'未配置！！请检查！！', key)
    REF_FILENAME = os.path.abspath(data[key])
    key = 'excel_info_file'
    if key not in data:
        ec_converter.logger.error('\'settings.json\'中的\'%s\'未配置！！请检查！！', key)
    EXCEL_INFO_FILENAME = os.path.abspath(data[key])
    key = 'data_list_name'
    if key not in data:
        ec_converter.logger.error('\'settings.json\'中的\'%s\'未配置！！请检查！！', key)
    DATA_LIST_NAME = data[key]
    key = 'dump_file_ext_name'
    if key not in data:
        ec_converter.logger.error('\'settings.json\'中的\'%s\'未配置！！请检查！！', key)
    DUMP_FILE_EXT_NAME = data[key]
    key = 'indent_char'
    if key not in data:
        ec_converter.logger.error('\'settings.json\'中的\'%s\'未配置！！请检查！！', key)
    INDENT_CHAR = data[key]
    key = 'quotation_marks'
    if key not in data:
        ec_converter.logger.error('\'settings.json\'中的\'%s\'未配置！！请检查！！', key)
    QUOTATION_MARKS = data[key]
    key = 'dump_list_as_tuple'
    if key not in data:
        ec_converter.logger.error('\'settings.json\'中的\'%s\'未配置！！请检查！！', key)
    DUMP_LIST_AS_TUPLE = data[key]
    key = 'dump_ch_name'
    if key not in data:
        ec_converter.logger.error('\'settings.json\'中的\'%s\'未配置！！请检查！！', key)
    DUMP_CH_NAME = data[key]
    key = 'ref_splitter'
    if key not in data:
        ec_converter.logger.error('\'settings.json\'中的\'%s\'未配置！！请检查！！', key)
    REF_SPLITTER = data[key]
    key = 'default_splitter'
    if key not in data:
        ec_converter.logger.error('\'settings.json\'中的\'%s\'未配置！！请检查！！', key)
    DEFAULT_SPLITTER = data[key]
    key = 'field_name_splitter'
    if key not in data:
        ec_converter.logger.error('\'settings.json\'中的\'%s\'未配置！！请检查！！', key)
    FIELD_NAME_SPLITTER = data[key]
    key = 'repeated_value_splitter'
    if key not in data:
        ec_converter.logger.error('\'settings.json\'中的\'%s\'未配置！！请检查！！', key)
    REPEATED_VALUE_SPLITTER = data[key]
    key = 'data_name_splitter'
    if key not in data:
        ec_converter.logger.error('\'settings.json\'中的\'%s\'未配置！！请检查！！', key)
    DATA_NAME_SPLITTER = data[key]
    key = 'field_text_index'
    if key not in data:
        ec_converter.logger.error('\'settings.json\'中的\'%s\'未配置！！请检查！！', key)
    FIELD_TEXT_INDEX = data[key]
    key = 'field_name_index'
    if key not in data:
        ec_converter.logger.error('\'settings.json\'中的\'%s\'未配置！！请检查！！', key)
    FIELD_NAME_INDEX = data[key]
    key = 'field_type_index'
    if key not in data:
        ec_converter.logger.error('\'settings.json\'中的\'%s\'未配置！！请检查！！', key)
    FIELD_TYPE_INDEX = data[key]
    key = 'field_label_index'
    if key not in data:
        ec_converter.logger.error('\'settings.json\'中的\'%s\'未配置！！请检查！！', key)
    FIELD_LABEL_INDEX = data[key]
    key = 'field_default_index'
    if key not in data:
        ec_converter.logger.error('\'settings.json\'中的\'%s\'未配置！！请检查！！', key)
    FIELD_DEFAULT_INDEX = data[key]
    key = 'row_offset'
    if key not in data:
        ec_converter.logger.error('\'settings.json\'中的\'%s\'未配置！！请检查！！', key)
    ROW_OFFSET = data[key]
    key = 'column_offset'
    if key not in data:
        ec_converter.logger.error('\'settings.json\'中的\'%s\'未配置！！请检查！！', key)
    COLUMN_OFFSET = data[key]
    key = 'data_name_coordinate'
    if key not in data:
        ec_converter.logger.error('\'settings.json\'中的\'%s\'未配置！！请检查！！', key)
    DATA_NAME_COORDINATE = data[key]
    key = 'data_name_suffix'
    if key not in data:
        ec_converter.logger.error('\'settings.json\'中的\'%s\'未配置！！请检查！！', key)
    DATA_NAME_SUFFIX = data[key]
    key = 'id_column_name'
    if key not in data:
        ec_converter.logger.error('\'settings.json\'中的\'%s\'未配置！！请检查！！', key)
    ID_COLUMN_NAME = data[key]
    key = 'ch_name_column_name'
    if key not in data:
        ec_converter.logger.error('\'settings.json\'中的\'%s\'未配置！！请检查！！', key)
    CH_NAME_COLUMN_NAME = data[key]
    key = 'repeatable_field_name_in_splitted_sheets'
    if key not in data:
        ec_converter.logger.error('\'settings.json\'中的\'%s\'未配置！！请检查！！', key)
    REPEATABLE_FIELD_NAME_IN_SPLITTED_SHEETS = data[key]
