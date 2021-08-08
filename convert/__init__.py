# -*- coding: utf-8 -*-
# author: Tac
# contact: gzzhanghuaxiong@corp.netease.com

import ec_converter
import convert.common_helper
import convert.reference_handler
import convert.converter
import convert.info_generator
import convert.dump_handler


@convert.common_helper.time_it
def convert_data(file_list):
    """
    导表入口函数
    Args:
        file_list: [list]每一项是要导表的excel文件的完整路径
    Returns:
        bool是否成功
    """
    ec_converter.logger.info('开始对下列Excel文件执行导表程序：\n%s', '\n'.join(file_list))

    convert.reference_handler.load_ref_data(file_list)
    for file in file_list:
        # for-else就是如果for过程中被break了else就不跑，如果for全部没有break就跑else
        if not convert.converter.convert_excel_file(file):
            ec_converter.logger.error('导表失败!!!')
            return False
    else:
        convert.dump_handler.dump_data_list()
        ec_converter.logger.info('导表成功!!!')
    return True


@convert.common_helper.time_it
def generate_excel_info():
    """
    生成项目的excel信息
    Returns:
        bool是否成功
    """
    ec_converter.logger.info('开始生成项目Excel信息')

    convert.info_generator.gen_ref_file()
    convert.info_generator.gen_data_info()

    return True
