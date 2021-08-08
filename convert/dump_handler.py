# -*- coding: utf-8 -*-
# author: Tac
# contact: gzzhanghuaxiong@corp.netease.com

import os

import jinja2

import ec_converter
import settings
import const
import convert.formatter

jinja_env = None  # type: jinja2.Environment


def dump_data_module(excel_file_path, data_name, sheet_result):
    """
    dump一个data文件
    Args:
        excel_file_path: [str]excel完整路径
        data_name: [str]导出的data模块名
        sheet_result: data_name对应的convert.sheet_result.SheetResult实例
    Returns:
        None
    """
    excel_file_name = os.path.basename(excel_file_path)

    data = {}
    for row_data in sheet_result.data_list:
        if settings.ID_COLUMN_NAME not in row_data:
            raise KeyError('缺少字段: %s' % settings.ID_COLUMN_NAME)
        id_value = row_data[settings.ID_COLUMN_NAME]
        if id_value in data:
            raise KeyError('%s重复: %s' % settings.ID_COLUMN_NAME, id_value)
        data[id_value] = row_data

    import convert.converter
    translate_meta_info = convert.converter.get_translate_meta_info(sheet_result)

    _init_jinja_env()
    template = jinja_env.get_template(const.TemplateName.DATA_MODULE)
    content = template.render(
        excel_file_name=excel_file_name,
        data=data,
        translate_meta_info=translate_meta_info,
    )

    dump_file_basename = '%s.%s' % (data_name, settings.DUMP_FILE_EXT_NAME)
    dump_file_path = os.path.join(settings.OUTPUT_DIR, dump_file_basename)
    _dump_file(dump_file_path, content)


def dump_data_list():
    """
    dump data_list文件
    Returns:
        None
    """
    ec_converter.logger.info('dump %s', settings.DATA_LIST_NAME)
    data_list = []
    for root, _, files in os.walk(settings.OUTPUT_DIR):
        for file_name in files:
            valid_suffix = '%s.%s' % (settings.DATA_NAME_SUFFIX, settings.DUMP_FILE_EXT_NAME)
            if not file_name.endswith(valid_suffix):
                continue
            file_path = os.path.join(root, file_name)
            module_name = file_path.replace(settings.OUTPUT_DIR, '').replace('\\', '/').replace(
                '.%s' % settings.DUMP_FILE_EXT_NAME, '').replace('/', '.')
            if module_name.startswith('.'):
                module_name = module_name[len('.'):]
            data_list.append(module_name)
    data_list.sort(key=lambda s: s.lower())

    _init_jinja_env()
    template = jinja_env.get_template(const.TemplateName.DATA_LIST)
    content = template.render(data_list=data_list)

    dump_file_basename = '%s.%s' % (settings.DATA_LIST_NAME, settings.DUMP_FILE_EXT_NAME)
    dump_file_path = os.path.join(settings.OUTPUT_DIR, dump_file_basename)
    _dump_file(dump_file_path, content)


def dump_ref_file(content):
    """
    dump引用信息文件
    Args:
        content: [str]文件内容
    Returns:
        None
    """
    _dump_file(settings.REF_FILENAME, content)


def dump_excel_info_file(content):
    """
    dump所有Excel信息的文件
    Args:
        content: [str]文件内容
    Returns:
        None
    """
    _dump_file(settings.EXCEL_INFO_FILENAME, content)


def _init_jinja_env():
    """
    初始化jinja2环境
    Returns:
        None
    """
    global jinja_env
    if jinja_env:
        return
    curr_dir_name = os.path.dirname(__file__)
    template_dir_name = os.path.join(curr_dir_name, const.JINJA_TEMPLATES_DIR_NAME)
    loader = jinja2.FileSystemLoader(template_dir_name)
    jinja_env = jinja2.Environment(loader=loader)
    jinja_env.filters[const.FORMATTER_FILTER_NAME] = convert.formatter.format_data


def _dump_file(file_path, content, encoding='utf-8'):
    """
    dump一个文件
    Args:
        file_path: [str]文件完整路径
        content: [str]文件内容
        encoding: [str]文件编码格式
    Returns:
        None
    """
    dirname = os.path.dirname(file_path)
    if not os.path.exists(dirname):
        # 目录没有创建则不dump
        ec_converter.logger.error('dump失败, 目录: \'%s\' 不存在', dirname)
        return
    assert isinstance(content, str)
    with open(file_path, 'w', encoding=encoding) as f:
        f.write(content)
