# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import os

import genv
from const import convert_const
from . import common_helper, excel_handler, reference_handler


@common_helper.time_it
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
    selections = [data[genv.settings.id_column_name] for data in data_list]
    comment = '\n'.join(
        f'{data[genv.settings.id_column_name]}: {data.get(genv.settings.enum_comment_column_name, "")}' for data in data_list)
    enum_key = f'{enum_name}{genv.settings.enum_key_splitter}{enum_class_name}'
    validation_dict = reference_handler.ENUM_VALIDATION_DICT.get(enum_key, {})
    if not validation_dict:
        return
    for ref_excel_file, file_validation_list in validation_dict.items():
        if not file_validation_list:
            continue

        ref_file_path = os.path.join(genv.settings.excel_dir, ref_excel_file)
        workbook = excel_handler.get_workbook(ref_file_path)
        modified = False
        for validation_info in file_validation_list:
            sheet_name = validation_info[convert_const.ValidationInfoKey.SHEET_NAME]
            col_idx = validation_info[convert_const.ValidationInfoKey.COLUMN_INDEX]
            sheet = excel_handler.get_sheet_by_name(workbook, sheet_name)
            modified = excel_handler.set_column_validator_type_list(sheet, col_idx, selections, genv.settings.row_offset)
            modified = excel_handler.set_worksheet_cell_value(sheet, genv.settings.field_text_index - 1, col_idx, comment)
            modified = excel_handler.set_worksheet_cell_comment(sheet, genv.settings.field_text_index, col_idx, comment, enum_key)

        if modified:
            try:
                workbook.save(ref_file_path)
            except IOError:
                genv.logger.error('\'%s\'在你的本地处于编辑状态, 无法写入validator, 请将其关掉后重试', ref_excel_file)
        workbook.close()
        del workbook
