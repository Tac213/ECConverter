# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com


class ColumnSchema(object):
    """
    抽象单个字段
    """

    def __init__(self, index: int, name: str, type_, label: str, default, translate_meta: str = None, ref: str = None):
        """
        构造器
        Args:
            index: [int]字段所在的列索引值
            name: [str]字段名
            type_: 字段类型, eval过
            label: [str]字段label
            default: 字段默认值
            translate_meta: [str]翻译元信息
            ref: [str]引用proto
        """
        self.index = index
        self.name = name
        self.type = type_
        self.label = label
        self.default = default
        self.translate_meta = translate_meta
        self.ref = ref
        self.additional_import = None  # 字段需要额外导入的模块名，是个str
