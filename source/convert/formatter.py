# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import genv
from const import convert_const


def format_data(data, indent_count: int = 0) -> str:
    """
    将py数据格式化为字符串, 类似json.dumps
    因为语法是确定的, 所以这里很多字符串就写死了, 不写到const里了
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
        if genv.settings.id_column_name in keys:
            # 把id排在第一位
            keys.remove(genv.settings.id_column_name)
            keys.insert(0, genv.settings.id_column_name)
        for key in keys:
            assert isinstance(key, (bool, int, float, str, tuple))
            value = format_data(data[key], indent_count + 1)
            key = format_data(key)
            if key == format_data(genv.settings.ch_name_column_name) and genv.settings.dump_ch_name:
                output.append(f'{(indent_count + 1) * genv.settings.indent_char}# {key}: {value},')
            else:
                output.append(f'{(indent_count + 1) * genv.settings.indent_char}{key}: {value},')
        output.append(indent_count * genv.settings.indent_char + '}')
    elif isinstance(data, (tuple, list)):
        if genv.settings.dump_list_as_tuple:
            output.append('(')
        else:
            output.append('[')
        for value in data:
            value = format_data(value, indent_count + 1)
            output.append(f'{(indent_count + 1) * genv.settings.indent_char}{value},')
        if genv.settings.dump_list_as_tuple:
            output.append(indent_count * genv.settings.indent_char + ')')
        else:
            output.append(indent_count * genv.settings.indent_char + ']')
    elif isinstance(data, str):
        for prefix in convert_const.SPECIAL_STR_PREFIX:
            if data.startswith(prefix):
                output.append(data)
                break
        else:
            output.append(f'{genv.settings.quotation_marks}{data}{genv.settings.quotation_marks}')
    elif isinstance(data, (bool, int, float)):
        output.append(str(data))
    else:
        raise ValueError(f'不支持的数据类型: {data.__class__.__name__}')
    return '\n'.join(output)
