# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import os

import jinja2

import genv
from const import convert_const, path_const
from . import formatter, sheet_result

jinja_env = None  # type: jinja2.Environment


def render_enum_class(**render_kwargs):
    """
    render生成enum的类代码
    Args:
        render_kwargs: [dict]render代码时的kwargs
    Returns:
        str
    """
    _init_jinja_env()
    template = jinja_env.get_template(convert_const.TemplateName.ENUM_CLASS)
    return template.render(**render_kwargs)


def dump_enum_module(enum_name: str, class_code_list: list) -> None:
    """
    dump一个enum文件
    Args:
        enum_name: [str]导出的enum的模块名
        class_code_list: [list]类代码列表
    Returns:
        None
    """
    if enum_name not in genv.settings.enum_info:
        genv.logger.error('enum名字\'%s\'错误, dump失败', enum_name)
        return
    if convert_const.ENUM_OUTPUT_DIR_KEY not in genv.settings.enum_info[enum_name]:
        genv.logger.error('\'%s\'的%s未配置, dump失败', enum_name, convert_const.ENUM_OUTPUT_DIR_KEY)
        return
    output_dir = os.path.abspath(genv.settings.enum_info[enum_name][convert_const.ENUM_OUTPUT_DIR_KEY])
    _init_jinja_env()
    template = jinja_env.get_template(convert_const.TemplateName.ENUM_MODULE)
    content = template.render(
        module_name=enum_name,
        class_code_list=class_code_list,
    )
    dump_file_basename = f'{enum_name}{genv.settings.dump_file_ext_name}'
    dump_file_path = os.path.join(output_dir, dump_file_basename)
    _dump_file(dump_file_path, content)


def dump_data_module(excel_file_path: str, data_name: str, result: sheet_result.SheetResult) -> None:
    """
    dump一个data文件
    Args:
        excel_file_path: [str]excel完整路径
        data_name: [str]导出的data模块名
        result: data_name对应的convert.sheet_result.SheetResult实例
    Returns:
        None
    """
    excel_file_name = os.path.basename(excel_file_path)

    data = {}
    for row_data in result.data_list:
        if genv.settings.id_column_name not in row_data:
            raise KeyError(f'缺少字段: {genv.settings.id_column_name}')
        id_value = row_data[genv.settings.id_column_name]
        if id_value in data:
            raise KeyError(f'{genv.settings.id_column_name}重复: {id_value}')
        data[id_value] = row_data

    from . import converter  # pylint: disable=import-outside-toplevel
    translate_meta_info = converter.get_translate_meta_info(result)
    addtional_import_info = converter.get_addtional_import_info(result)

    _init_jinja_env()
    template = jinja_env.get_template(convert_const.TemplateName.DATA_MODULE)
    content = template.render(
        excel_file_name=excel_file_name,
        data=data,
        translate_meta_info=translate_meta_info,
        addtional_import_info=addtional_import_info,
    )

    dump_file_basename = f'{data_name}{genv.settings.dump_file_ext_name}'
    dump_file_path = os.path.join(genv.settings.output_dir, dump_file_basename)
    _dump_file(dump_file_path, content)


def dump_data_list() -> None:
    """
    dump data_list文件
    Returns:
        None
    """
    genv.logger.info('dump %s', genv.settings.data_list_name)
    data_list = []
    for root, _, files in os.walk(genv.settings.output_dir):
        for file_name in files:
            valid_suffix = f'{genv.settings.data_name_suffix}{genv.settings.dump_file_ext_name}'
            if not file_name.endswith(valid_suffix):
                continue
            file_path = os.path.normpath(os.path.join(root, file_name))
            file_relpath = os.path.relpath(file_path, genv.settings.output_dir)
            module_name = file_relpath.replace(genv.settings.dump_file_ext_name, '').replace(os.path.sep, '.')
            if module_name.startswith('.'):
                module_name = module_name[len('.'):]
            data_list.append(module_name)
    data_list.sort(key=lambda s: s.lower())

    _init_jinja_env()
    template = jinja_env.get_template(convert_const.TemplateName.DATA_LIST)
    content = template.render(data_list=data_list)

    dump_file_basename = f'{genv.settings.data_list_name}{genv.settings.dump_file_ext_name}'
    dump_file_path = os.path.join(genv.settings.output_dir, dump_file_basename)
    _dump_file(dump_file_path, content)


def dump_ref_file(content: str) -> None:
    """
    dump引用信息文件
    Args:
        content: [str]文件内容
    Returns:
        None
    """
    _dump_file(genv.settings.ref_file, content)


def dump_enum_ref_file(content: str) -> None:
    """
    dump enum引用信息文件
    Args:
        content: [str]文件内容
    Returns:
        None
    """
    _dump_file(genv.settings.enum_ref_file, content)


def dump_excel_info_file(content: str) -> None:
    """
    dump所有Excel信息的文件
    Args:
        content: [str]文件内容
    Returns:
        None
    """
    _dump_file(genv.settings.excel_info_file, content)


def dump_enum_info_file(content: str) -> None:
    """
    dump所有enum信息的文件
    Args:
        content: [str]文件内容
    Returns:
        None
    """
    _dump_file(genv.settings.enum_info_file, content)


def _init_jinja_env() -> None:
    """
    初始化jinja2环境
    Returns:
        None
    """
    global jinja_env
    if jinja_env:
        return
    loader = jinja2.FileSystemLoader(path_const.TEMPLATE_DIR)
    jinja_env = jinja2.Environment(loader=loader)
    jinja_env.filters[convert_const.FORMATTER_FILTER_NAME] = formatter.format_data


def _dump_file(file_path: str, content: str, encoding: str = 'utf-8') -> None:
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
        genv.logger.error('dump失败, 目录: \'%s\' 不存在', dirname)
        return
    assert isinstance(content, str)
    with open(file_path, 'w', encoding=encoding) as f:
        f.write(content)
