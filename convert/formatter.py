# -*- coding: utf-8 -*-
# author: Tac
# contact: gzzhanghuaxiong@corp.netease.com

import settings


def format_data(data, indent_count=0):
    """
    将py数据格式化为字符串, 类似json.dumps
    因为语法是确定的，所以这里很多字符串就写死了，不写到const里了
    Args:
        data: bool/int/float/str/list/dict
        indent_count: [int]缩进数量
    Returns:
        str
    """
    output = []
    if isinstance(data, dict):
        output.append('{')
        keys = sorted(data.keys())
        if settings.ID_COLUMN_NAME in keys:
            # 把id排在第一位
            keys.remove(settings.ID_COLUMN_NAME)
            keys.insert(0, settings.ID_COLUMN_NAME)
        for key in keys:
            assert isinstance(key, (bool, int, float, str, tuple))
            value = format_data(data[key], indent_count + 1)
            key = format_data(key)
            if key == format_data(settings.CH_NAME_COLUMN_NAME) and settings.DUMP_CH_NAME:
                output.append('%s# %s: %s,' % ((indent_count + 1) * settings.INDENT_CHAR, key, value))
            else:
                output.append('%s%s: %s,' % ((indent_count + 1) * settings.INDENT_CHAR, key, value))
        output.append(indent_count * settings.INDENT_CHAR + '}')
    elif isinstance(data, (tuple, list)):
        if settings.DUMP_LIST_AS_TUPLE:
            output.append('(')
        else:
            output.append('[')
        for value in data:
            value = format_data(value, indent_count + 1)
            output.append('%s%s,' % ((indent_count + 1) * settings.INDENT_CHAR, value))
        if settings.DUMP_LIST_AS_TUPLE:
            output.append(indent_count * settings.INDENT_CHAR + ')')
        else:
            output.append(indent_count * settings.INDENT_CHAR + ']')
    elif isinstance(data, str):
        output.append('%s%s%s' % (settings.QUOTATION_MARKS, data, settings.QUOTATION_MARKS))
    elif isinstance(data, (bool, int, float)):
        output.append(str(data))
    else:
        raise ValueError('不支持的数据类型: %s' % type(data))
    return '\n'.join(output)
