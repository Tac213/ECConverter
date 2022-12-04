# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import typing
import os

import genv
from const import convert_const
from . import excel_handler, common_helper, column_schema

INDEX_DICT = {}
ENUM_INDEX_DICT = {}
ENUM_VALIDATION_DICT = {}


def _gen_index_dict(referred_file_list: typing.List[str]) -> None:
    """
    生成index dict
    Args:
        referred_file_list: [list]每一项是Excel表的绝对路径
    Returns:
        None
    """
    INDEX_DICT.clear()
    for filename in referred_file_list:
        workbook = excel_handler.get_workbook(filename)
        for sheet in excel_handler.get_sheets(workbook):
            data_name = excel_handler.get_data_name(sheet)
            if data_name is None:
                continue
            original_data_name = data_name
            if genv.settings.data_name_splitter in data_name:
                data_name = data_name.split(genv.settings.data_name_splitter)[0]
            id_name = excel_handler.get_cell_value_str(sheet, genv.settings.field_name_index, genv.settings.column_offset)
            id_type = excel_handler.get_cell_value_str(sheet, genv.settings.field_type_index, genv.settings.column_offset)
            for col_idx, col_values in enumerate(excel_handler.get_col_generator(sheet, genv.settings.column_offset),
                                                 genv.settings.column_offset):
                cell_value_str = excel_handler.get_cell_value_str_with_tuple(col_values, genv.settings.field_name_index)
                if cell_value_str == genv.settings.ch_name_column_name:
                    name_name = cell_value_str
                    name_idx = col_idx
                    break
            else:
                raise KeyError(f'\'{filename}的\'{data_name}\'缺少字段: \'{genv.settings.ch_name_column_name}\'')
            if id_name != genv.settings.id_column_name:
                continue
            if name_name != genv.settings.ch_name_column_name:
                continue
            for row_values in excel_handler.get_row_generator(sheet, genv.settings.row_offset):
                id_value = excel_handler.get_cell_value_str_with_tuple(row_values, genv.settings.column_offset)
                name_value = excel_handler.get_cell_value_str_with_tuple(row_values, name_idx)
                if not id_value or not name_value:
                    continue
                if id_type == 'int':
                    id_value = int(id_value)
                data_dict = INDEX_DICT.setdefault(data_name, {})
                if name_value in data_dict:
                    prev_id = data_dict[name_value]
                    if prev_id != id_value:
                        raise Exception(f'ch_name冲突, data_name: {original_data_name}, ch_name: {name_value}, id: {id_value}')
                data_dict[name_value] = id_value
        workbook.close()
        del workbook


def _gen_enum_index_dict(refered_enum_list: typing.List[str]) -> None:
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
    ENUM_INDEX_DICT.clear()
    for enum_dir_name in refered_enum_list:
        enum_path = os.path.join(genv.settings.excel_dir, enum_dir_name)
        file_list = os.listdir(enum_path)
        for file_name in file_list:
            if not file_name.endswith('.xlsx') or file_name.startswith('~'):
                continue
            file_path = os.path.join(enum_path, file_name)
            workbook = excel_handler.get_workbook(file_path)
            sheets = excel_handler.get_sheets(workbook)
            for sheet in sheets:
                class_name = excel_handler.get_enum_class_name(sheet)
                sheet_name = excel_handler.get_sheet_name(sheet)
                if not class_name:
                    continue
                id_name = excel_handler.get_cell_value_str(sheet, genv.settings.field_name_index, genv.settings.column_offset)
                id_type = excel_handler.get_cell_value_str(sheet, genv.settings.field_type_index, genv.settings.column_offset)
                assert id_type == 'str'
                value_name = excel_handler.get_cell_value_str(sheet, genv.settings.field_name_index, genv.settings.enum_value_column_index)
                value_type = excel_handler.get_cell_value_str(sheet, genv.settings.field_type_index, genv.settings.enum_value_column_index)
                if id_name != genv.settings.id_column_name:
                    continue
                if value_name != genv.settings.enum_value_column_name:
                    continue
                enum_key = f'{enum_dir_name}{genv.settings.enum_key_splitter}{class_name}'
                for row_values in excel_handler.get_row_generator(sheet, genv.settings.row_offset):
                    id_value = excel_handler.get_cell_value_str_with_tuple(row_values, genv.settings.column_offset)
                    value_value = excel_handler.get_cell_value_str_with_tuple(row_values, genv.settings.enum_value_column_index)
                    if not id_value or not value_value:
                        continue
                    if value_type == 'int':
                        value_value = int(value_value)
                    enum_dict = ENUM_INDEX_DICT.setdefault(enum_key, {})
                    if id_value in enum_dict:
                        prev_value = enum_dict[id_value]
                        if prev_value != value_value:
                            raise Exception(
                                f'!!!enum的value冲突, class_name: {enum_key}, id: {id_value}, value: {value_value}, last_value: {prev_value}, sheet_name: {sheet_name}'  # pylint: disable=line-too-long
                            )
                    enum_dict[id_value] = value_value

            workbook.close()
            del workbook


def _get_refered_enum_list(file_list: typing.List[str]) -> typing.List[str]:
    """
    获取引用的enum目录名列表
    Args:
        file_list: [list]每一项是Excel表的绝对路径
    Returns:
        list, 每一项是str, enum目录名
    """
    with open(genv.settings.enum_ref_file, 'r', encoding='utf-8') as f:
        readlines = f.readlines()

    # 读取ENUM_REF_FILENAME得到excel引用到enum引用的关系
    enum_ref_dict = {}
    for line in readlines:
        line_split = line.split(convert_const.REF_FILE_SPLITER)
        if len(line_split) != convert_const.EnumRefInfoIndex.LENGTH:
            continue
        from_file = line_split[convert_const.EnumRefInfoIndex.FROM_EXCEL].strip()
        to_enum = line_split[convert_const.EnumRefInfoIndex.TO_EXCEL].strip().split(genv.settings.enum_path_splitter)[0]
        to_enum_set = enum_ref_dict.setdefault(from_file, set())  # type: set
        to_enum_set.add(to_enum)

    refered_enum_set = set()
    for file_name in file_list:
        basename = os.path.basename(file_name)
        refered_set = enum_ref_dict.get(basename, set())
        refered_enum_set.update(refered_set)

    return list(refered_enum_set)


def _get_referred_file_list(file_list: typing.List[str]) -> typing.List[str]:
    """
    根据要导的表，得到所有被引用的表
    Args:
        file_list: [list]每一项是Excel表的绝对路径
    Returns:
        list, 每一项是Excel表的绝对路径
    """
    dirname = os.path.dirname(genv.settings.ref_file)
    with open(genv.settings.ref_file, 'r', encoding='utf-8') as f:
        readlines = f.readlines()

    file_ref_dict = {}
    for line in readlines:
        line_split = line.split(convert_const.REF_FILE_SPLITER)
        if len(line_split) != convert_const.RefInfoIndex.LENGTH:
            continue
        from_excel_name = line_split[convert_const.RefInfoIndex.FROM_EXCEL].strip()
        to_excel_name = line_split[convert_const.RefInfoIndex.TO_EXCEL].strip()
        to_file_set = file_ref_dict.setdefault(from_excel_name, set())  # type: set
        to_file_set.add(os.path.join(dirname, to_excel_name))

    referred_file_set = set()
    for filename in file_list:
        basename = os.path.basename(filename)
        referred_set = file_ref_dict.get(basename, set())
        referred_file_set.update(referred_set)

    return list(referred_file_set)


@common_helper.time_it
def load_ref_data(file_list: typing.List[str]) -> None:
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


def gen_enum_validation_dict() -> None:
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
    ENUM_VALIDATION_DICT.clear()
    with open(genv.settings.enum_ref_file, 'r', encoding='utf-8') as f:
        readlines = f.readlines()

    # 读取enum_ref_file得到enum到excel的映射信息
    for line in readlines:
        line_split = line.split(convert_const.REF_FILE_SPLITER)
        if len(line_split) != convert_const.EnumRefInfoIndex.LENGTH:
            continue
        to_file = line_split[convert_const.EnumRefInfoIndex.FROM_EXCEL].strip()
        sheet_name = line_split[convert_const.EnumRefInfoIndex.FROM_SHEET].strip()
        col_idx = line_split[convert_const.EnumRefInfoIndex.COLUMN_IDX].strip()
        from_enum = line_split[convert_const.EnumRefInfoIndex.TO_CLASS].strip()
        validation_dict = ENUM_VALIDATION_DICT.setdefault(from_enum, {})  # type: dict
        file_validation_list = validation_dict.setdefault(to_file, [])  # type: list
        file_validation_list.append({
            convert_const.ValidationInfoKey.SHEET_NAME: sheet_name,
            convert_const.ValidationInfoKey.COLUMN_INDEX: int(col_idx),
        })


def replace_reference(col_schema: column_schema.ColumnSchema, value: typing.Any) -> typing.Any:
    """
    将ch_name替换成id
    Args:
        column_schema: ColumnSchema实例
        value: 读表的值
    Returns:
        ch_name对应的id
    """
    if isinstance(value, list):
        new_value = [_get_ref_value(col_schema.ref, val) for val in value]
    else:
        new_value = _get_ref_value(col_schema.ref, value)
    return new_value


def _get_ref_value(ref_data_name: str, name_value: str) -> typing.Any:
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
        raise Exception(f'无效的引用: \'{name_value}\', 在Data: \'{ref_data_name}\'中')
    return id_value


def _get_enum_ref_value(enum_key: str, enum_id: str) -> typing.Any:
    """
    获取enum引用对应的值
    Args:
        enum_key: [str]enum类对应的key, 比如'xxxconst.ClassName'
        enum_id: [str]成员名id
    Returns:
        enum_key.enum_id真正的值
    """
    value = ENUM_INDEX_DICT.get(enum_key, {}).get(enum_id, None)
    if value is None:
        raise Exception(f'无效的引用: \'{enum_id}\', 在enum: \'{enum_key}\'中')
    return value
