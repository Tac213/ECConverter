# -*- coding: utf-8 -*-
# author: Tac
# contact: gzzhanghuaxiong@corp.netease.com

import os

import settings
import const
import convert.excel_handler
import convert.dump_handler


def gen_ref_file():
    """
    生成引用文件
    Returns:
        None
    """
    file_list = os.listdir(settings.EXCEL_DIR)

    # 先生成映射关系
    data_name_to_excel_name = {}  # data_name到excel_name的映射关系
    for file_name in file_list:
        if not file_name.endswith('.xlsx') or file_name.startswith('~'):
            continue
        file_path = os.path.join(settings.EXCEL_DIR, file_name)
        workbook = convert.excel_handler.get_workbook(file_path)
        sheets = convert.excel_handler.get_sheets(workbook)
        for sheet in sheets:
            data_name = convert.excel_handler.get_data_name(sheet)
            if not data_name:
                continue
            if settings.DATA_NAME_SPLITTER in data_name:
                data_name = data_name.split(settings.DATA_NAME_SPLITTER)[0]
            data_name_to_excel_name[data_name] = file_name

        workbook.close()
        del workbook

    content = []  # 最后生成的文件内容
    for file_name in file_list:
        if not file_name.endswith('.xlsx') or file_name.startswith('~'):
            continue
        file_path = os.path.join(settings.EXCEL_DIR, file_name)
        workbook = convert.excel_handler.get_workbook(file_path)
        sheets = convert.excel_handler.get_sheets(workbook)
        for sheet in sheets:
            data_name = convert.excel_handler.get_data_name(sheet)
            for _, col_values in enumerate(convert.excel_handler.get_col_generator(sheet, settings.COLUMN_OFFSET),
                                           settings.COLUMN_OFFSET):
                field_name = convert.excel_handler.get_cell_value_str_with_tuple(col_values, settings.FIELD_NAME_INDEX)
                field_type = convert.excel_handler.get_cell_value_str_with_tuple(col_values, settings.FIELD_TYPE_INDEX)
                if settings.REF_SPLITTER not in field_type:
                    continue
                _, field_reference = field_type.split(settings.REF_SPLITTER)
                content.append(const.REF_FILE_LINE_FORMAT % (file_name, data_name, field_name,
                                                             field_type, field_reference,
                                                             data_name_to_excel_name[field_reference]))

        workbook.close()
        del workbook

    content.append('')  # 最后加一个空行
    convert.dump_handler.dump_ref_file('\n'.join(content))


def gen_data_info():
    """
    生成项目所有Excel的信息
    Returns:
        None
    """
    file_list = os.listdir(settings.EXCEL_DIR)

    content = []  # 最后生成的文件内容
    for file_name in file_list:
        if not file_name.endswith('.xlsx') or file_name.startswith('~'):
            continue
        file_path = os.path.join(settings.EXCEL_DIR, file_name)
        workbook = convert.excel_handler.get_workbook(file_path)
        sheets = convert.excel_handler.get_sheets(workbook)
        line_content = [file_name]
        for sheet in sheets:
            data_name = convert.excel_handler.get_data_name(sheet)
            if not data_name:
                continue
            if settings.DATA_NAME_SPLITTER in data_name:
                data_name = data_name.split(settings.DATA_NAME_SPLITTER)[0]
            if data_name not in line_content:
                line_content.append(data_name)
        if len(line_content) > 1:
            content.append(const.EXCEL_INFO_SPLITER.join(line_content))

        workbook.close()
        del workbook

    content.append('')  # 最后加一个空行
    convert.dump_handler.dump_excel_info_file('\n'.join(content))
