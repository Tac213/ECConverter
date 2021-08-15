# -*- coding: utf-8 -*-
# author: Tac
# contact: gzzhanghuaxiong@corp.netease.com

import os

import convert.excel_handler
import convert.common_helper
import settings
import const

INDEX_DICT = {}


def _gen_index_dict(referred_file_list):
    """
    生成index dict
    Args:
        referred_file_list: [list]每一项是Excel表的绝对路径
    Returns:
        None
    """
    global INDEX_DICT
    INDEX_DICT.clear()
    for filename in referred_file_list:
        workbook = convert.excel_handler.get_workbook(filename)
        for sheet in convert.excel_handler.get_sheets(workbook):
            data_name = convert.excel_handler.get_data_name(sheet)
            if data_name is None:
                continue
            original_data_name = data_name
            if settings.DATA_NAME_SPLITTER in data_name:
                data_name = data_name.split(settings.DATA_NAME_SPLITTER)[0]
            id_name = convert.excel_handler.get_cell_value_str(sheet, settings.FIELD_NAME_INDEX, settings.COLUMN_OFFSET)
            id_type = convert.excel_handler.get_cell_value_str(sheet, settings.FIELD_TYPE_INDEX, settings.COLUMN_OFFSET)
            name_name = convert.excel_handler.get_cell_value_str(sheet,
                                                                 settings.FIELD_NAME_INDEX, settings.COLUMN_OFFSET + 1)
            if id_name != settings.ID_COLUMN_NAME:
                continue
            if name_name != settings.CH_NAME_COLUMN_NAME:
                continue
            for row_values in convert.excel_handler.get_row_generator(sheet, settings.ROW_OFFSET):
                id_value = row_values[settings.COLUMN_OFFSET]
                name_value = row_values[settings.COLUMN_OFFSET + 1]
                if not id_value or not name_value:
                    continue
                if id_type == 'int':
                    assert isinstance(id_value, int), \
                        'id类型错误，data_name: %s, ch_name: %s, id: %s' % (original_data_name, name_value, id_value)
                data_dict = INDEX_DICT.setdefault(data_name, {})
                if name_value in data_dict:
                    prev_id = data_dict[name_value]
                    if prev_id != id_value:
                        raise Exception('ch_name冲突，data_name: %s, ch_name: %s, id: %s'
                                        % (original_data_name, name_value, id_value))
                data_dict[name_value] = id_value
        workbook.close()
        del workbook


def _get_referred_file_list(file_list):
    """
    根据要导的表，得到所有被引用的表
    Args:
        file_list: [list]每一项是Excel表的绝对路径
    Returns:
        list, 每一项是Excel表的绝对路径
    """
    dirname = os.path.dirname(settings.REF_FILENAME)
    with open(settings.REF_FILENAME, 'r', encoding='utf-8') as f:
        readlines = f.readlines()

    file_ref_dict = {}
    for line in readlines:
        line_split = line.split(const.REF_FILE_SPLITER)
        if len(line_split) != const.RefInfoIndex.LENGTH:
            continue
        from_excel_name = line_split[const.RefInfoIndex.FROM_EXCEL].strip()
        to_excel_name = line_split[const.RefInfoIndex.TO_EXCEL].strip()
        to_file_set = file_ref_dict.setdefault(from_excel_name, set())
        to_file_set.add(os.path.join(dirname, to_excel_name))

    referred_file_set = set()
    for filename in file_list:
        basename = os.path.basename(filename)
        referred_set = file_ref_dict.get(basename, set())
        referred_file_set.update(referred_set)

    return list(referred_file_set)


@convert.common_helper.time_it
def load_ref_data(file_list):
    """
    根据要导的表，加载被引用的表的数据，结果存在全局变量里
    Args:
        file_list: [list]每一项是Excel表的绝对路径
    Returns:
        None
    """
    referred_file_list = _get_referred_file_list(file_list)
    if not referred_file_list:
        return
    _gen_index_dict(referred_file_list)


def replace_reference(column_schema, value):
    """
    将ch_name替换成id
    Args:
        column_schema: ColumnSchema实例
        value: 读表的值
    Returns:
        tuple
        0: id的值的类型
        1: ch_name对应的id
    """
    if isinstance(value, list):
        new_value = [_get_ref_value(column_schema.ref, val) for val in value]
    else:
        new_value = _get_ref_value(column_schema.ref, value)
    return type(new_value), new_value


def _get_ref_value(ref_data_name, name_value):
    """
    获取引用值对应的id
    Args:
        ref_data_name: [str]引用的data名
        name_value: [str]ch_name
    Returns:
        ch_name对应的id
    """
    id_value = INDEX_DICT.get(ref_data_name, {}).get(name_value, None)
    if id_value is None:
        raise Exception('无效的引用: \'%s\'，在Data: \'%s\'中' % (name_value, ref_data_name))
    return id_value
