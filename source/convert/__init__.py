# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import typing
import os
import genv
from . import common_helper, reference_handler, converter, info_generator, dump_handler


@common_helper.time_it
def convert_data(file_list: typing.List[str]) -> bool:
    """
    导表入口函数
    Args:
        file_list: [list]每一项是要导表的excel文件的相对路径
    Returns:
        bool是否成功
    """
    file_list = [os.path.join(genv.settings.excel_dir, file_path) for file_path in file_list]
    genv.logger.info('开始对下列Excel文件执行导表程序:\n%s', '\n'.join(file_list))

    reference_handler.load_ref_data(file_list)
    for file_path in file_list:
        # for-else就是如果for过程中被break了else就不跑，如果for全部没有break就跑else
        try:
            if not converter.convert_excel_file(file_path):
                genv.logger.error('导表失败!!!')
                return False
        except Exception:  # pylint: disable=broad-except
            genv.logger.log_last_except()
            genv.logger.error('导表失败!!!')
            return False
    else:
        dump_handler.dump_data_list()
        genv.logger.info('导表成功!!!')
    return True


@common_helper.time_it
def convert_enum(enum_list: typing.List[str], is_set_data_validation: bool) -> bool:
    """
    导出enum入口函数
    Args:
        enum_list: [list]每一项是要导出的enum目录的相对路径
        is_set_data_validation: [bool]是否为引用excel设置数据验证
    Returns:
        bool是否成功
    """
    enum_list = [os.path.join(genv.settings.excel_dir, enum_path) for enum_path in enum_list]
    genv.logger.info('开始对下列enum目录执行导表程序:\n%s', '\n'.join(enum_list))

    if is_set_data_validation:
        reference_handler.gen_enum_validation_dict()

    for enum_dir_name in enum_list:
        # for-else就是如果for过程中被break了else就不跑，如果for全部没有break就跑else
        try:
            if not converter.convert_enum_dir(enum_dir_name, is_set_data_validation):
                genv.logger.error('导出enum失败!!!')
                return False
        except Exception:  # pylint: disable=broad-except
            genv.logger.log_last_except()
            genv.logger.error('导出enum失败!!!')
            return False
    else:
        genv.logger.info('导出enum成功!!!')
    return True


@common_helper.time_it
def generate_excel_info() -> bool:
    """
    生成项目的excel信息
    Returns:
        bool是否成功
    """
    genv.logger.info('开始生成项目Excel信息')

    try:
        info_generator.gen_ref_file()
        info_generator.gen_data_info()
    except Exception:  # pylint: disable=broad-except
        genv.logger.log_last_except()
        genv.logger.error('生成项目Excel信息失败!!!')
        return False

    return True


@common_helper.time_it
def generate_enum_info() -> bool:
    """
    生成项目的enum信息
    Returns:
        bool是否成功
    """
    genv.logger.info('开始生成项目enum信息')

    try:
        info_generator.gen_ref_file()
        info_generator.gen_enum_info()
    except Exception:  # pylint: disable=broad-except
        genv.logger.log_last_except()
        genv.logger.error('生成项目enum信息失败!!!')
        return False

    return True
