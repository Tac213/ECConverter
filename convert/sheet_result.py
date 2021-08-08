# -*- coding: utf-8 -*-
# author: Tac
# contact: gzzhanghuaxiong@corp.netease.com


class SheetResult(object):
    """
    抽象单个sheet的导表结果
    """

    def __init__(self, data_name):
        """
        构造器
        Args:
            data_name: [str]sheet对应的data名字
        """
        self.data_name = data_name
        self.data_list = []  # 每一行导出的结果

        self.name_schema_dict = {}  # 字段名到schema对象的映射关系
        self.col_schema_dict = {}  # 列索引值到schema对象的映射关系
