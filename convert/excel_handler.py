# -*- coding: utf-8 -*-
# author: Tac
# contact: gzzhanghuaxiong@corp.netease.com

import openpyxl

import const
import settings


def get_workbook(excel_path):
    """
    读取Excel的工作簿，而且只读取数据
    Args:
        excel_path: [str]excel完整路径
    Returns:
        openpyxl.workbook.Workbook
    """
    return openpyxl.load_workbook(excel_path, read_only=False, data_only=True)


def get_sheets(workbook):
    """
    读取工作簿的所有sheet
    Args:
        workbook: openpyxl.workbook.Workbook
    Returns:
        list, 每一项是openpyxl.worksheet.worksheet.Worksheet
    """
    return workbook.worksheets


def get_data_name(sheet):
    """
    获取某一页sheet对应的data名字
    Args:
        sheet: openpyxl.worksheet.worksheet.Worksheet
    Returns:
        str
    """
    data_name = get_cell_value_str(sheet, *settings.DATA_NAME_COORDINATE)
    if not data_name.endswith(settings.DATA_NAME_SUFFIX):
        return None
    return data_name


def get_row_generator(sheet, start_idx):
    """
    获取行的生成器，用于遍历sheet
    Args:
        sheet: openpyxl.worksheet.worksheet.Worksheet
        start_idx: [int]起始索引值，索引值从0开始
    Returns:
        types.GeneratorType
    """
    return sheet.iter_rows(min_row=start_idx + 1, values_only=True)


def get_col_generator(sheet, start_idx):
    """
    获取行的生成器，用于遍历sheet
    Args:
        sheet: openpyxl.worksheet.worksheet.Worksheet
        start_idx: [int]起始索引值，索引值从0开始
    Returns:
        types.GeneratorType
    """
    return sheet.iter_cols(min_col=start_idx + 1, values_only=True)


def get_sheet_name(sheet):
    """
    获取sheet名字
    Args:
        sheet: openpyxl.worksheet.worksheet.Worksheet
    Returns:
        types.GeneratorType
    """
    return sheet.title


def get_sheet_row_count(sheet):
    """
    获取sheet的行数
    Args:
        sheet: openpyxl.worksheet.worksheet.Worksheet
    Returns:
        int
    """
    return len([_ for _ in sheet.rows])


def get_sheet_column_count(sheet):
    """
    获取sheet的行数
    Args:
        sheet: openpyxl.worksheet.worksheet.Worksheet
    Returns:
        int
    """
    return len([_ for _ in sheet.columns])


def get_cell_value(sheet, row_idx, col_idx):
    """
    获取单元格数据
    Args:
        sheet: openpyxl.worksheet.worksheet.Worksheet
        row_idx: [int]行索引值，索引值从0开始
        col_idx: [int]列索引值，索引值从0开始
    Returns:
        sheet原本的数据
    """
    return sheet.cell(row_idx + 1, col_idx + 1).value


def get_value_str(value):
    """
    将excel原始数据转为字符串
    Args:
        value: excel数据
    Returns:
        str, 经过字符串处理的数据
    """
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        import math
        if math.fabs(value - int(value)) < const.INT_THRESHOLD:
            value = str(int(value))
        else:
            value = str(value)
        return value
    if value is None:
        return ''
    return str(value).strip()


def get_cell_value_str(sheet, row_idx, col_idx):
    """
    获取经过字符串处理的单元格数据
    Args:
        sheet: openpyxl.worksheet.worksheet.Worksheet
        row_idx: [int]行索引值，索引值从0开始
        col_idx: [int]列索引值，索引值从0开始
    Returns:
        str, 经过字符串处理的单元格数据
    """
    value = get_cell_value(sheet, row_idx, col_idx)
    return get_value_str(value)


def get_cell_value_str_with_tuple(row_or_col_data_tuple, idx):
    """
    通过生成器得到的行数据或列数据元组，获取经过字符串处理的单元格数据
    Args:
        row_or_col_data_tuple: [tuple]通过生成器得到的行数据或列数据元组
        idx: [int]索引值，从0开始
    Returns:
        str, 经过字符串处理的单元格数据
    """
    value = row_or_col_data_tuple[idx]
    return get_value_str(value)


def get_column_name(col_idx):
    """
    根据列索引值获取列名
    Args:
        col_idx:
    Returns:
        str
    """
    return openpyxl.utils.get_column_letter(col_idx)


def get_cell_name(row_idx, col_idx):
    """
    获取单元格名字
    Args:
        row_idx: [int]行索引值，索引值从0开始
        col_idx: [int]列索引值，索引值从0开始
    Returns:
        str
    """
    return '%s%s' % (get_column_name(col_idx), row_idx + 1)
