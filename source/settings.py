# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import typing
import dataclasses
import os
import json

from const import path_const


@dataclasses.dataclass
class ECConverterSettings(object):

    # 表所在目录，是个绝对路径，json里填相对路径
    excel_dir: str
    # 导表输出文件目录，是个绝对路径，json里填相对路径
    output_dir: str
    # 引用信息文件，是个绝对路径，json里填相对路径
    ref_file: str
    # enum引用信息文件，是个绝对路径，json里填相对路径
    enum_ref_file: str
    # 所有Excel信息的文件，是个绝对路径，json里填相对路径
    excel_info_file: str
    # 所有enum信息的文件，是个绝对路径，json里填相对路径
    enum_info_file: str
    # data list的模块名
    data_list_name: str
    # dump文件的拓展名
    dump_file_ext_name: str
    # 缩进字符
    indent_char: str
    # 引号
    quotation_marks: str
    # dump的时候是否以tuple的格式dump list
    dump_list_as_tuple: bool
    # dump的时候是否注释掉ch_name
    dump_ch_name: bool
    # 引用表的分隔符
    ref_splitter: str
    # 默认值的分隔符
    default_splitter: str
    # 字段名的分隔符
    field_name_splitter: str
    # repeated值的分隔符
    repeated_value_splitter: str
    # data名的分隔符
    data_name_splitter: str
    # enum key的分隔符, 比如uconst.ClassName, 分隔符就是'.'
    enum_key_splitter: str
    # enum路径的分隔符，比如uconst/00-测试.xlsx, 分隔符就是'/'
    enum_path_splitter: str
    # 字段文本所在的行的索引值
    field_text_index: int
    # 字段名所在的行的索引值
    field_name_index: int
    # 字段类型所在的行的索引值
    field_type_index: int
    # 字段label所在的行的索引值
    field_label_index: int
    # 字段默认值所在的行的索引值
    field_default_index: int
    # 数据开始行索引值
    row_offset: int
    # 数据开始列索引值
    column_offset: int
    # enum的value字段列索引值
    enum_value_column_index: int
    # data名字的坐标
    data_name_coordinate: typing.List[int]
    # data名字的后缀
    data_name_suffix: str
    # id的字段名
    id_column_name: str
    # ch_name的字段名
    ch_name_column_name: str
    # enum的value的字段名
    enum_value_column_name: str
    # enum注释的字段名
    enum_comment_column_name: str
    # 在拆分工作表时允许重复的字段名
    repeatable_field_name_in_splitted_sheets: typing.List[str]
    # enum的相关信息，key为enum的名字，value为字典
    enum_info: typing.Dict[str, typing.Dict[str, str]]

    def resolve_paths(self) -> 'ECConverterSettings':
        """
        resolve all paths to abspath
        """
        if not os.path.isabs(self.excel_dir):
            self.excel_dir = os.path.normpath(os.path.join(path_const.ROOT_DIR, self.excel_dir))
        if not os.path.isabs(self.output_dir):
            self.output_dir = os.path.normpath(os.path.join(path_const.ROOT_DIR, self.output_dir))
        if not os.path.isabs(self.ref_file):
            self.ref_file = os.path.normpath(os.path.join(path_const.ROOT_DIR, self.ref_file))
        if not os.path.isabs(self.enum_ref_file):
            self.enum_ref_file = os.path.normpath(os.path.join(path_const.ROOT_DIR, self.enum_ref_file))
        if not os.path.isabs(self.excel_info_file):
            self.excel_info_file = os.path.normpath(os.path.join(path_const.ROOT_DIR, self.excel_info_file))
        if not os.path.isabs(self.enum_info_file):
            self.enum_info_file = os.path.normpath(os.path.join(path_const.ROOT_DIR, self.ref_file))
        return self


def initialize_settings() -> ECConverterSettings:
    settings_json_file_path = os.path.join(path_const.ROOT_DIR, 'settings.json')
    with open(settings_json_file_path, 'r', encoding='utf-8') as fp:
        data = json.load(fp)
    return ECConverterSettings(**data).resolve_paths()
