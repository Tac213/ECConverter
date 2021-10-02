# -*- coding: utf-8 -*-
# author: Tac
# contact: gzzhanghuaxiong@corp.netease.com

import os

import convert.excel_handler
import convert.common_helper
import settings
import const

INDEX_DICT = {}
ENUM_INDEX_DICT = {}
ENUM_VALIDATION_DICT = {}


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
            for col_idx, col_values in enumerate(convert.excel_handler.get_col_generator(sheet, settings.COLUMN_OFFSET),
                                                 settings.COLUMN_OFFSET):
                cell_value_str = convert.excel_handler.get_cell_value_str_with_tuple(col_values,
                                                                                     settings.FIELD_NAME_INDEX)
                if cell_value_str == settings.CH_NAME_COLUMN_NAME:
                    name_name = cell_value_str
                    name_idx = col_idx
                    break
            else:
                raise KeyError('\'%s\'的\'%s\'缺少字段: \'%s\'' % (filename, data_name, settings.CH_NAME_COLUMN_NAME))
            if id_name != settings.ID_COLUMN_NAME:
                continue
            if name_name != settings.CH_NAME_COLUMN_NAME:
                continue
            for row_values in convert.excel_handler.get_row_generator(sheet, settings.ROW_OFFSET):
                id_value = convert.excel_handler.get_cell_value_str_with_tuple(row_values, settings.COLUMN_OFFSET)
                name_value = convert.excel_handler.get_cell_value_str_with_tuple(row_values, name_idx)
                if not id_value or not name_value:
                    continue
                if id_type == 'int':
                    id_value = int(id_value)
                data_dict = INDEX_DICT.setdefault(data_name, {})
                if name_value in data_dict:
                    prev_id = data_dict[name_value]
                    if prev_id != id_value:
                        raise Exception('ch_name冲突，data_name: %s, ch_name: %s, id: %s'
                                        % (original_data_name, name_value, id_value))
                data_dict[name_value] = id_value
        workbook.close()
        del workbook


def _gen_enum_index_dict(refered_enum_list):
    """
    生成EnumIndexDict
    数据结构:
    {
        'xxxconst.ClassName': {
            id_value: value_value,
        },
    }
    Args:
        refered_enum_list: [list]每一项是str, enum目录名
    Returns:
        None
    """
    global ENUM_INDEX_DICT
    ENUM_INDEX_DICT.clear()
    for enum_dir_name in refered_enum_list:
        enum_path = os.path.join(settings.EXCEL_DIR, enum_dir_name)
        file_list = os.listdir(enum_path)
        for file_name in file_list:
            if not file_name.endswith('.xlsx') or file_name.startswith('~'):
                continue
            file_path = os.path.join(enum_path, file_name)
            workbook = convert.excel_handler.get_workbook(file_path)
            sheets = convert.excel_handler.get_sheets(workbook)
            for sheet in sheets:
                class_name = convert.excel_handler.get_enum_class_name(sheet)
                sheet_name = convert.excel_handler.get_sheet_name(sheet)
                if not class_name:
                    continue
                id_name = convert.excel_handler.get_cell_value_str(sheet, settings.FIELD_NAME_INDEX,
                                                                   settings.COLUMN_OFFSET)
                id_type = convert.excel_handler.get_cell_value_str(sheet, settings.FIELD_TYPE_INDEX,
                                                                   settings.COLUMN_OFFSET)
                assert id_type == 'str'
                value_name = convert.excel_handler.get_cell_value_str(sheet, settings.FIELD_NAME_INDEX,
                                                                      settings.ENUM_VALUE_COLUMN_INDEX)
                value_type = convert.excel_handler.get_cell_value_str(sheet, settings.FIELD_TYPE_INDEX,
                                                                      settings.ENUM_VALUE_COLUMN_INDEX)
                if id_name != settings.ID_COLUMN_NAME:
                    continue
                if value_name != settings.ENUM_VALUE_COLUMN_NAME:
                    continue
                enum_key = '%s%s%s' % (enum_dir_name, settings.ENUM_KEY_SPLITTER, class_name)
                for row_values in convert.excel_handler.get_row_generator(sheet, settings.ROW_OFFSET):
                    id_value = convert.excel_handler.get_cell_value_str_with_tuple(row_values, settings.COLUMN_OFFSET)
                    value_value = convert.excel_handler.get_cell_value_str_with_tuple(row_values,
                                                                                      settings.ENUM_VALUE_COLUMN_INDEX)
                    if not id_value or not value_value:
                        continue
                    if value_type == 'int':
                        value_value = int(value_value)
                    enum_dict = ENUM_INDEX_DICT.setdefault(enum_key, {})
                    if id_value in enum_dict:
                        prev_value = enum_dict[id_value]
                        if prev_value != value_value:
                            raise Exception(
                                '!!!enum的value冲突, class_name: %s, id: %s, value: %s, last_value: %s, sheet_name:%s' %
                                (enum_key, id_value, value_value, prev_value, sheet_name))
                    enum_dict[id_value] = value_value

            workbook.close()
            del workbook


def _get_refered_enum_list(file_list):
    """
    获取引用的enum目录名列表
    Args:
        file_list: [list]每一项是Excel表的绝对路径
    Returns:
        list, 每一项是str, enum目录名
    """
    with open(settings.ENUM_REF_FILENAME, 'r', encoding='utf-8') as f:
        readlines = f.readlines()

    # 读取ENUM_REF_FILENAME得到excel引用到enum引用的关系
    enum_ref_dict = {}
    for line in readlines:
        line_split = line.split(const.REF_FILE_SPLITER)
        if len(line_split) != const.EnumRefInfoIndex.LENGTH:
            continue
        from_file = line_split[const.EnumRefInfoIndex.FROM_EXCEL].strip()
        to_enum = line_split[const.EnumRefInfoIndex.TO_EXCEL].strip().split(settings.ENUM_PATH_SPLITTER)[0]
        to_enum_set = enum_ref_dict.setdefault(from_file, set())
        to_enum_set.add(to_enum)

    refered_enum_set = set()
    for file_name in file_list:
        basename = os.path.basename(file_name)
        refered_set = enum_ref_dict.get(basename, set())
        refered_enum_set.update(refered_set)

    return list(refered_enum_set)


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
    refered_enum_list = _get_refered_enum_list(file_list)
    if refered_enum_list:
        _gen_enum_index_dict(refered_enum_list)
    referred_file_list = _get_referred_file_list(file_list)
    if not referred_file_list:
        return
    _gen_index_dict(referred_file_list)


def gen_enum_validation_dict():
    """
    加载config.ENUM_VALIDATION_DICT
    数据结构:
    {
        'xxx_enum.ClassName': {
            '00-测试.xlsx': [
                'sheet_name': sheet_name,
                'col_idx': col_idx,
            ],
        },
    }
    Returns:
        None
    """
    global ENUM_VALIDATION_DICT
    ENUM_VALIDATION_DICT.clear()
    with open(settings.ENUM_REF_FILENAME, 'r', encoding='utf-8') as f:
        readlines = f.readlines()

    # 读取enum_ref_file得到enum到excel的映射信息
    for line in readlines:
        line_split = line.split(const.REF_FILE_SPLITER)
        if len(line_split) != const.EnumRefInfoIndex.LENGTH:
            continue
        to_file = line_split[const.EnumRefInfoIndex.FROM_EXCEL].strip()
        sheet_name = line_split[const.EnumRefInfoIndex.FROM_SHEET].strip()
        col_idx = line_split[const.EnumRefInfoIndex.COLUMN_IDX].strip()
        from_enum = line_split[const.EnumRefInfoIndex.TO_CLASS].strip()
        validation_dict = ENUM_VALIDATION_DICT.setdefault(from_enum, {})
        file_validation_list = validation_dict.setdefault(to_file, [])
        file_validation_list.append({
            const.ValidationInfoKey.SHEET_NAME: sheet_name,
            const.ValidationInfoKey.COLUMN_INDEX: int(col_idx),
        })


def replace_reference(column_schema, value):
    """
    将ch_name替换成id
    Args:
        column_schema: ColumnSchema实例
        value: 读表的值
    Returns:
        ch_name对应的id
    """
    if isinstance(value, list):
        new_value = [_get_ref_value(column_schema.ref, val) for val in value]
    else:
        new_value = _get_ref_value(column_schema.ref, value)
    return new_value


def _get_ref_value(ref_data_name, name_value):
    """
    获取引用值对应的id
    Args:
        ref_data_name: [str]引用的data名
        name_value: [str]ch_name
    Returns:
        ch_name对应的id
    """
    if ref_data_name in ENUM_INDEX_DICT:
        return _get_enum_ref_value(ref_data_name, name_value)
    id_value = INDEX_DICT.get(ref_data_name, {}).get(name_value, None)
    if id_value is None:
        raise Exception('无效的引用: \'%s\'，在Data: \'%s\'中' % (name_value, ref_data_name))
    return id_value


def _get_enum_ref_value(enum_key, enum_id):
    """
    获取enum引用对应的值
    Args:
        enum_key: [str]enum类对应的key，比如'xxxconst.ClassName'
        enum_id: [str]成员名id
    Returns:
        enum_key.enum_id真正的值
    """
    value = ENUM_INDEX_DICT.get(enum_key, {}).get(enum_id, None)
    if value is None:
        raise Exception('无效的引用: \'%s\'，在enum: \'%s\'中' % (enum_id, enum_key))
    return value

