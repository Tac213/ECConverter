# -*- coding: utf-8 -*-
# author: Tac
# contact: gzzhanghuaxiong@corp.netease.com

import os.path

import convert.common_helper
import convert.excel_handler
from convert.reference_handler import ENUM_VALIDATION_DICT
import settings
import const
import ec_converter


@convert.common_helper.time_it
def handle_validation(enum_name, enum_class_name, data_list):
    """
    处理某个enum sheet的validation
    Args:
        enum_name: [str]enum的模块名
        enum_class_name: [str]enum的类名
        data_list: [list]enum类的导表结果
    Returns:
        None
    """
    selections = [data[settings.ID_COLUMN_NAME] for data in data_list]
    comment = '\n'.join(
        '%s: %s' %
        (data[settings.ID_COLUMN_NAME], data.get(settings.ENUM_COMMENT_COLUMN_NAME, '')) for data in data_list
    )
    enum_key = '%s%s%s' % (enum_name, settings.ENUM_KEY_SPLITTER, enum_class_name)
    validation_dict = ENUM_VALIDATION_DICT.get(enum_key, {})
    if not validation_dict:
        return
    for ref_excel_file, file_validation_list in validation_dict.items():
        if not file_validation_list:
            continue

        ref_file_path = os.path.join(settings.EXCEL_DIR, ref_excel_file)
        workbook = convert.excel_handler.get_workbook(ref_file_path)
        modified = False
        for validation_info in file_validation_list:
            sheet_name = validation_info[const.ValidationInfoKey.SHEET_NAME]
            col_idx = validation_info[const.ValidationInfoKey.COLUMN_INDEX]
            sheet = convert.excel_handler.get_sheet_by_name(workbook, sheet_name)
            modified = convert.excel_handler.set_column_validator_type_list(sheet, col_idx, selections)
            modified = convert.excel_handler.set_worksheet_cell_value(sheet, settings.FIELD_TEXT_INDEX - 1,
                                                                      col_idx, comment)
            modified = convert.excel_handler.set_worksheet_cell_comment(sheet, settings.FIELD_TEXT_INDEX,
                                                                        col_idx, comment, enum_key)

        if modified:
            try:
                workbook.save(ref_file_path)
            except IOError:
                ec_converter.logger.error('\'%s\'在你的本地处于编辑状态，无法写入validator，请将其关掉后重试', ref_excel_file)
        workbook.close()
        del workbook
