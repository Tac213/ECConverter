# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import typing
from . import column_schema


class SheetResult(object):
    """
    抽象单个sheet的导表结果
    """

    def __init__(self, data_name: str):
        """
        构造器
        Args:
            data_name: [str]sheet对应的data名字
        """
        self.data_name = data_name
        self.data_list: typing.List[dict] = []  # 每一行导出的结果

        self.name_schema_dict: typing.Dict[str, column_schema.ColumnSchema] = {}  # 字段名到schema对象的映射关系
        self.col_schema_dict: typing.Dict[int, column_schema.ColumnSchema] = {}  # 列索引值到schema对象的映射关系
