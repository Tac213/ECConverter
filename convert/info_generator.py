# -*- coding: utf-8 -*-
# author: Tac
# contact: gzzhanghuaxiong@corp.netease.com

import os

import ec_converter
import settings
import const
import convert.excel_handler
import convert.dump_handler


def gen_ref_file():
    """
    生成引用文件, 包括普通引用和enum引用
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

    enum_class_name_to_excel_name = {}  # enum类名到excel_name的映射关系
    for enum_name in settings.ENUM_INFO.keys():
        enum_file_list = os.listdir(os.path.join(settings.EXCEL_DIR, enum_name))
        for file_name in enum_file_list:
            if not file_name.endswith('.xlsx') or file_name.startswith('~'):
                continue
            file_path = os.path.join(settings.EXCEL_DIR, enum_name, file_name)
            workbook = convert.excel_handler.get_workbook(file_path)
            sheets = convert.excel_handler.get_sheets(workbook)
            for sheet in sheets:
                enum_class_name = convert.excel_handler.get_enum_class_name(sheet)
                if not enum_class_name:
                    continue
                enum_key = '%s%s%s' % (enum_name, settings.ENUM_KEY_SPLITTER, enum_class_name)
                enum_path = '%s%s%s' % (enum_name, settings.ENUM_PATH_SPLITTER, file_name)
                enum_class_name_to_excel_name[enum_key] = enum_path

            workbook.close()
            del workbook

    content = []  # 最后生成的文件内容
    enum_content = []  # enum文件内容
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
            sheet_name = convert.excel_handler.get_sheet_name(sheet)
            for idx, col_values in enumerate(convert.excel_handler.get_col_generator(sheet, settings.COLUMN_OFFSET),
                                             settings.COLUMN_OFFSET):
                field_name = convert.excel_handler.get_cell_value_str_with_tuple(col_values, settings.FIELD_NAME_INDEX)
                field_type = convert.excel_handler.get_cell_value_str_with_tuple(col_values, settings.FIELD_TYPE_INDEX)
                if settings.REF_SPLITTER not in field_type:
                    continue
                _, field_reference = field_type.split(settings.REF_SPLITTER)
                if field_reference in enum_class_name_to_excel_name:
                    enum_line = const.ENUM_REF_FILE_LINE_FORMAT % (file_name, sheet_name, data_name, idx, field_name,
                                                                   field_type, field_reference,
                                                                   enum_class_name_to_excel_name[field_reference])
                    enum_content.append(enum_line)
                elif field_reference in data_name_to_excel_name:
                    content.append(const.REF_FILE_LINE_FORMAT % (file_name, data_name, field_name,
                                                                 field_type, field_reference,
                                                                 data_name_to_excel_name[field_reference]))
                else:
                    ec_converter.logger.error('excel文件\'%s\'的%s存在错误的引用: \'%s\'',
                                              file_name, sheet_name, field_reference)

        workbook.close()
        del workbook

    content.append('')  # 最后加一个空行
    convert.dump_handler.dump_ref_file('\n'.join(content))
    enum_content.append('')  # 最后加一个空行
    convert.dump_handler.dump_enum_ref_file('\n'.join(enum_content))


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


def gen_enum_info():
    """
    生成项目所有enum的信息
    Returns:
        None
    """
    content = []  # 最后生成的文件内容
    for enum_name in settings.ENUM_INFO.keys():
        file_list = os.listdir(os.path.join(settings.EXCEL_DIR, enum_name))
        for file_name in file_list:
            if not file_name.endswith('.xlsx') or file_name.startswith('~'):
                continue
            file_path = os.path.join(settings.EXCEL_DIR, enum_name, file_name)
            workbook = convert.excel_handler.get_workbook(file_path)
            sheets = convert.excel_handler.get_sheets(workbook)
            enum_path = '%s%s%s' % (enum_name, settings.ENUM_PATH_SPLITTER, file_name)
            line_content = [enum_path]
            for sheet in sheets:
                class_name = convert.excel_handler.get_enum_class_name(sheet)
                if not class_name:
                    continue
                if class_name not in line_content:
                    line_content.append(class_name)
            if len(line_content) > 1:
                content.append(const.EXCEL_INFO_SPLITER.join(line_content))

            workbook.close()
            del workbook

    content.append('')  # 最后加一个空行
    convert.dump_handler.dump_enum_info_file('\n'.join(content))
