# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com
"""
提供一些钩子
钩子会在导表的一些特定阶段被调用
可以利用钩子对表最终导出的数据进行特殊处理
因为属于特殊处理所以可以写一些硬编码
"""

from . import sheet_result


def pre_dump_hook(data_name: str, result: sheet_result.SheetResult):
    """
    在将表的数据dump成文件之前会被调用的钩子
    可以在这个钩子里对sheet_result做处理, 改变dump出来的数据结构
    Args:
        data_name: [str]各拆分sheet合成之后的真正的data_name
        result: data_name对应的convert.sheet_result.SheetResult实例
    Returns:
        None
    """
