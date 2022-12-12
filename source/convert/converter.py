# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import typing
import os
import time
import datetime

import genv
from const import convert_const
from . import common_helper, excel_handler, dump_handler, sheet_result, column_schema, reference_handler, validation_handler, hooks

unique_id_check_dict = {}  # 检查id是否重复的字典, key为data_name，value为对应的id的集合


@common_helper.time_it
def convert_sheet(sheet, result_dict: dict, is_enum_mode: bool = False) -> bool:
    """
    转换单个sheet的数据
    Args:
        sheet: openpyxl.worksheet.worksheet.Worksheet
        result_dict: [dict]结果都存在这里, key为data_name, value为sheet_result
        is_enum_mode: [bool]是否为enum导表模式
    Returns:
        bool, 是否成功
    """
    if is_enum_mode:
        data_name = excel_handler.get_enum_class_name(sheet)
    else:
        data_name = excel_handler.get_data_name(sheet)
    sheet_name = excel_handler.get_sheet_name(sheet)
    if not data_name:
        genv.logger.info('sheet \'%s\' 的data名字为空或不符合命名规则, 不导表', sheet_name)
        return True

    if data_name in result_dict:
        genv.logger.error('data名字 \'%s\' 重复, sheet name = \'%s\'', data_name, sheet_name)
        return False

    name_schema_dict = {}
    col_schema_dict = {}
    if not _get_sheet_schema_meta_info(sheet, name_schema_dict, col_schema_dict):
        genv.logger.error('sheet \'%s\' 获取字段信息失败', sheet_name)
        return False

    result = result_dict.setdefault(data_name, sheet_result.SheetResult(data_name))  # type: sheet_result.SheetResult
    result.name_schema_dict = name_schema_dict
    result.col_schema_dict = col_schema_dict

    for row_data in excel_handler.get_row_generator(sheet, genv.settings.row_offset):
        if not _convert_row(row_data, sheet_name, result):
            return False

    return True


@common_helper.time_it
def convert_excel_file(excel_file_path: str) -> bool:
    """
    转换excel数据
    Args:
        excel_file_path: [str]excel完整路径
    Returns:
        bool, 是否成功
    """
    genv.logger.info('开始导表: \'%s\'', excel_file_path)

    unique_id_check_dict.clear()

    workbook = excel_handler.get_workbook(excel_file_path)
    sheets = excel_handler.get_sheets(workbook)

    result_dict = {}  # type: typing.Dict[str, sheet_result.SheetResult]
    for sheet in sheets:
        if not convert_sheet(sheet, result_dict):
            genv.logger.error('导表失败, sheet name = \'%s\'', excel_handler.get_sheet_name(sheet))
            workbook.close()
            del workbook
            return False

    # excel用完了就关掉
    workbook.close()
    del workbook

    result_dict = _merge_sheets(result_dict)
    for data_name, result in result_dict.items():
        if not result.data_list:
            continue
        hooks.pre_dump_hook(data_name, result)

        dump_handler.dump_data_module(excel_file_path, data_name, result)

    return True


@common_helper.time_it
def convert_enum_excel_file(excel_file_path: str, is_set_data_validation: bool) -> typing.Optional[str]:
    """
    转换enum的excel数据为enum类代码
    Args:
        excel_file_path: [str]excel完整路径
        is_set_data_validation: [bool]是否为引用excel设置数据验证
    Returns:
        str, 类代码, 如果失败则返回None
    """
    genv.logger.info('开始导表: \'%s\'', excel_file_path)

    unique_id_check_dict.clear()

    enum_name = os.path.basename(os.path.dirname(excel_file_path))
    workbook = excel_handler.get_workbook(excel_file_path)
    sheets = excel_handler.get_sheets(workbook)

    result_dict = {}  # type: typing.Dict[str, sheet_result.SheetResult]
    enum_class_name_to_sheet_name = {}
    for sheet in sheets:
        enum_class_name = excel_handler.get_enum_class_name(sheet)
        sheet_name = excel_handler.get_sheet_name(sheet)
        enum_class_name_to_sheet_name[enum_class_name] = sheet_name
        if not convert_sheet(sheet, result_dict, True):
            genv.logger.error('导表失败, sheet name = \'%s\'', excel_handler.get_sheet_name(sheet))
            workbook.close()
            del workbook
            return None

    # excel用完了就关掉
    workbook.close()
    del workbook

    class_code_list = []
    for enum_class_name, result in result_dict.items():
        if not result.data_list:
            continue
        class_code = dump_handler.render_enum_class(
            class_name=enum_class_name,
            class_comment=enum_class_name_to_sheet_name[enum_class_name],
            members=result.data_list,
        )
        class_code_list.append(class_code)
        if is_set_data_validation:
            validation_handler.handle_validation(enum_name, enum_class_name, result.data_list)

    return '\n\n'.join(class_code_list)


@common_helper.time_it
def convert_enum_dir(enum_dir_path: str, is_set_data_validation: bool) -> bool:
    """
    转换单个enum目录的数据
    Args:
        enum_dir_path: [str]enum目录的完整路径
        is_set_data_validation: [bool]是否为引用excel设置数据验证
    Returns:
        bool, 是否成功
    """
    enum_name = os.path.basename(enum_dir_path)
    genv.logger.info('开始导出enum: \'%s\'', enum_name)
    enum_file_list = os.listdir(enum_dir_path)
    class_code_list = []
    for enum_excel in enum_file_list:
        if not enum_excel.endswith('.xlsx') or enum_excel.startswith('~'):
            continue
        excel_full_path = os.path.join(enum_dir_path, enum_excel)
        classes_code = convert_enum_excel_file(excel_full_path, is_set_data_validation)
        if classes_code is None:
            return False
        if classes_code:
            # 可能是空字符串导致多一个空行
            class_code_list.append(classes_code)
    dump_handler.dump_enum_module(enum_name, class_code_list)
    return True


def _convert_row(row_data: tuple, sheet_name: str, result: sheet_result.SheetResult) -> bool:
    """
    转换sheet某一行的数据, 结果存在sheet_result里
    Args:
        row_data: [tuple]该行的数据
        sheet_name: [str]sheet的名字, 主要用来显示错误信息
        sheet_result: SheetResult实例
    Returns:
        bool, 是否装欢成功
    """
    for idx, value in enumerate(row_data):
        if idx < genv.settings.column_offset:
            continue
        value_str = excel_handler.get_value_str(value)
        if value_str.strip() != '':
            break
    else:
        # 全部都是空字符串，空行不转任何数据
        return True

    data = {}
    for idx, value in enumerate(row_data):
        if idx < genv.settings.column_offset:
            continue
        col_schema = result.col_schema_dict.get(idx)
        if not col_schema:
            continue
        value_str = excel_handler.get_value_str(value)
        try:
            _fill_data_value(data, col_schema, value_str)
        except Exception as e:
            genv.logger.error('单元格解析失败, sheet = \'%s\', cell = \'%s\'', sheet_name, excel_handler.get_cell_name(idx, col_schema.index))
            raise e

    _post_process_data(data, result)

    return True


def get_translate_meta_info(result: sheet_result.SheetResult) -> typing.Dict[str, str]:
    """
    获取翻译元信息
    Args:
        sheet_result: SheetResult实例
    Returns:
        dict
    """
    translate_meta_info = {}
    for col_schema in result.name_schema_dict.values():
        if not col_schema.translate_meta:
            continue
        translate_meta_info[col_schema.name] = col_schema.translate_meta
    return translate_meta_info


def get_addtional_import_info(result: sheet_result.SheetResult) -> typing.List[str]:
    """
    获取额外导入信息
    Args:
        sheet_result: SheetResult实例
    Returns:
        list, 每一项是导入的模块名
    """
    import_info = []
    for col_schema in result.name_schema_dict.values():
        if not col_schema.additional_import:
            continue
        if col_schema.additional_import in import_info:
            continue
        import_info.append(col_schema.additional_import)
    return import_info


def _post_process_data(data: dict, result: sheet_result.SheetResult) -> None:
    """
    对导出的字典进行后处理
    Args:
        data: [dict]导出的字典数据
        sheet_result: SheetResult实例
    Returns:
        None
    """
    _merge_repeated_dict(data, result.name_schema_dict)

    if genv.settings.id_column_name not in data:
        raise AttributeError(f'必须要有{genv.settings.id_column_name}列')

    id_value = data[genv.settings.id_column_name]
    if id_value in unique_id_check_dict.get(result.data_name, {}):
        raise RuntimeError(f'{genv.settings.id_column_name}重复: {id_value}')
    unique_id_check_dict.setdefault(result.data_name, set()).add(id_value)

    # 检查id完成后保存该行结果
    result.data_list.append(data)


def _merge_repeated_dict(data: dict, name_schema_dict: typing.Dict[str, column_schema.ColumnSchema]) -> None:
    """
    对m_repeated的字段进行合成
    原本的data, 'xx.yy'这种字段，'xx'为key的value是个dict, 子dict的key是'yy', value是一个list
    合成之后，以'xx'为key的value变成list, list的每一项是个dict, dict的key为'yy'
    结果存在data里
    Args:
        data: [dict]导出的字典数据
        name_schema_dict: [dict]字段名到column_schema的映射关系
    Returns:
        None
    """
    for key, value in tuple(data.items()):
        if not isinstance(value, dict):
            continue
        for sub_key in value.keys():
            field_name = f'{key}{genv.settings.field_name_splitter}{sub_key}'
            col_schema = name_schema_dict.get(field_name)
            if not col_schema:
                # 可能是普通的dict字段，找不到col_schema
                break
            if not field_name:
                break
            if col_schema.label != convert_const.ValidFieldLabel.M_REPEATED:
                break
        else:
            # 全部都是m_repeated，可以merge
            merge_result = []  # type: typing.List[dict]
            for sub_key, sub_value in value.items():
                assert isinstance(sub_value, list)
                for idx, sub_value_item in enumerate(sub_value):
                    if idx >= len(merge_result):
                        merge_result.append({})
                    merge_result[idx].setdefault(sub_key, sub_value_item)
            data[key] = merge_result


def _merge_sheets(result_dict: typing.Dict[str, sheet_result.SheetResult]) -> typing.Dict[str, sheet_result.SheetResult]:
    """
    把同一份excel文件里面, aa_data.1/aa_data.2这种data合成同一份data
    Args:
        result_dict: [dict]单个excel导表结果, key为data_name, value为sheet_result
    Returns:
        dict, 合成后的结果, key为data_name, value为sheet_result
    """
    merged_result_dict = {}  # 合成后的结果, key为真正的data_name，value为sheet_result
    merged_cache_dict = {}  # 合成过程中的缓存，key为真正的data_name, value为字典，子字典的key为id，value为当前id合成后的导表结果
    merged_schema_dict = {}  # 合成后的name_schema_dict, key为真正的data_name, value为合成后的name_schame_dict
    for data_name, result in result_dict.items():
        if not result.data_list:
            continue
        if genv.settings.data_name_splitter in data_name:
            real_data_name = data_name.split(genv.settings.data_name_splitter)[0]
            merged_cache = merged_cache_dict.setdefault(real_data_name, {})
            _merge_splitted_sheets(merged_cache, result.data_list)
            merged_schema = merged_schema_dict.setdefault(real_data_name, {})  # type: dict
            merged_schema.update(result.name_schema_dict)
        else:
            merged_result_dict[data_name] = result

    for data_name, merged_cache in merged_cache_dict.items():
        merged_sheet_result = sheet_result.SheetResult(data_name)
        merged_sheet_result.name_schema_dict = merged_schema_dict[data_name]
        for row_data in merged_cache.values():
            merged_sheet_result.data_list.append(row_data)
        merged_result_dict[data_name] = merged_sheet_result

    return merged_result_dict


def _merge_splitted_sheets(merge_dict: typing.Dict[typing.Any, dict], data_list: typing.List[dict]) -> None:
    """
    获取被拆分的sheet后, 将其合在一起
    结果放在merge_dict里面
    Args:
        merge_dict: [dict]合成结果, key为id, value为合成后的数据字典
        data_list: [list]当前sheet的导表结果
    Returns:
        None
    """
    for data in data_list:
        if genv.settings.id_column_name not in data:
            continue
        id_value = data[genv.settings.id_column_name]
        if id_value in merge_dict:
            # 先检查表的拆分是否符合规则
            for field_name, field_value in data.items():
                if field_name == genv.settings.id_column_name:
                    continue
                if field_name not in genv.settings.repeatable_field_name_in_splitted_sheets and field_name in merge_dict[id_value]:
                    raise ValueError(f'拆分sheet时, 字段名重复。id: \'{id_value}\', 字段名: \'{field_name}\'')
                if field_name in merge_dict[id_value] and merge_dict[id_value][field_name] != field_value:
                    # settings.REPEATABLE_FIELD_NAME_IN_SPLITTED_SHEETS字段的值在拆分表里必须相同
                    raise ValueError(
                        f'拆分sheet时, {field_name}字段的{genv.settings.id_column_name}相同, 但值不同: [{merge_dict[id_value][field_name]} vs {field_value}]'  # pylint: disable=line-too-long
                    )

            merge_dict[id_value].update(data)
        else:
            merge_dict[id_value] = data


def _get_sheet_schema_meta_info(sheet, name_schema_dict: typing.Dict[str, column_schema.ColumnSchema],
                                col_schema_dict: typing.Dict[int, column_schema.ColumnSchema]) -> bool:
    """
    获取sheet的字段schema信息
    Args:
        sheet: openpyxl.worksheet.worksheet.Worksheet
        name_schema_dict: [dict]字段名到schema对象的映射关系
        col_schema_dict: [dict]列索引值到schema对象的映射关系
    Returns:
        bool, 是否获取成功
    """
    sheet_name = excel_handler.get_sheet_name(sheet)
    for idx, col_values in enumerate(excel_handler.get_col_generator(sheet, genv.settings.column_offset), genv.settings.column_offset):
        field_name = excel_handler.get_cell_value_str_with_tuple(col_values, genv.settings.field_name_index)
        field_type = excel_handler.get_cell_value_str_with_tuple(col_values, genv.settings.field_type_index)
        field_label = excel_handler.get_cell_value_str_with_tuple(col_values, genv.settings.field_label_index)
        field_default = excel_handler.get_cell_value_str_with_tuple(col_values, genv.settings.field_default_index)

        if field_name == '' or field_type == '' or field_label == '':
            break

        field_reference = None
        if genv.settings.ref_splitter in field_type:
            field_type, field_reference = field_type.split(genv.settings.ref_splitter)

        if field_type not in (convert_const.ValidFieldType.EVAL, convert_const.ValidFieldType.TIME, convert_const.ValidFieldType.DATETIME):
            try:
                field_type = eval(field_type)  # pylint: disable=eval-used
            except SyntaxError:
                genv.logger.error('暂不支持的字段类型: \'%s\', 在sheet \'%s\' 的字段 \'%s\' 中', field_type, sheet_name, field_name)
                return False

        if isinstance(field_type, type):
            if field_type not in (convert_const.ValidFieldType.BOOL, convert_const.ValidFieldType.INT, convert_const.ValidFieldType.FLOAT,
                                  convert_const.ValidFieldType.STR, convert_const.ValidFieldType.LIST, convert_const.ValidFieldType.DICT):
                genv.logger.error('sheet \'%s\' 的字段 \'%s\' 的类型填写错误', sheet_name, field_name)
                return False

        if field_label not in (convert_const.ValidFieldLabel.OPTIONAL, convert_const.ValidFieldLabel.REQUIRED,
                               convert_const.ValidFieldLabel.REPEATED, convert_const.ValidFieldLabel.M_REPEATED):
            genv.logger.error('sheet \'%s\'的字段 \'%s\'的label填写错误', sheet_name, field_name)
            return False

        translate_meta = None
        if genv.settings.default_splitter in field_default:
            field_default, translate_meta = field_default.split(genv.settings.default_splitter)
        if field_label == convert_const.ValidFieldLabel.REQUIRED and field_default != '':
            genv.logger.error('sheet \'%s\'的字段 \'%s\', label是required时不需要默认值', sheet_name, field_name)
            return False

        col_schema = column_schema.ColumnSchema(idx, field_name, field_type, field_label, field_default, translate_meta, field_reference)
        # 获取导表后的默认值
        field_default = _get_field_value(col_schema, field_default, True)
        col_schema.default = field_default
        if field_type in convert_const.ADDITIONAL_IMPORT_FIELD_TYPES:
            col_schema.additional_import = convert_const.ADDITIONAL_IMPORT_FIELD_TYPES[field_type]

        name_schema_dict[field_name] = col_schema
        col_schema_dict[idx] = col_schema

    return True


def _fill_data_value(data: dict, col_schema: column_schema.ColumnSchema, value_str: str) -> typing.Any:
    """
    在导表时填充data数据, 结果存在data里
    Args:
        data: [dict]单行导表结果
        col_schema: ColumnSchema实例
        value_str: [str]读表得到的经过字符串处理的值
    Returns:
        col_schema对应的value_str的值
    """
    value_str = value_str.strip()
    is_empty = not value_str

    field_name = col_schema.name
    sub_field_name = field_name

    if genv.settings.field_name_splitter in field_name and (not is_empty or col_schema.default != ''):
        field_name, sub_field_name = field_name.split(genv.settings.field_name_splitter)
        data = data.setdefault(field_name, {})

    field_name = sub_field_name
    value = _get_field_value(col_schema, value_str)

    if not is_empty:
        data[field_name] = value
    elif col_schema.default != '':
        # 用默认值填充空格子
        data[field_name] = col_schema.default

    return value


def _get_field_value(col_schema: column_schema.ColumnSchema, value_str: str, is_default_value: bool = False) -> typing.Any:
    """
    获取某个字段的值
    Args:
        col_schema: ColumnSchema实例
        value_str: [str]读表得到的经过字符串处理的值
        is_default_value: [bool]是否获取的是default的值
    Returns:
        col_schema对应的value_str的值
    """
    if col_schema.label == convert_const.ValidFieldLabel.REQUIRED:
        if not value_str:
            if is_default_value:
                return value_str
            else:
                raise AttributeError(f'required标签检查失败, 字段名: \'{col_schema.name}\'')

    if col_schema.label in (convert_const.ValidFieldLabel.OPTIONAL, convert_const.ValidFieldLabel.REPEATED,
                            convert_const.ValidFieldLabel.M_REPEATED):
        if not value_str:
            return value_str

    is_repeated = col_schema.label in (convert_const.ValidFieldLabel.REPEATED, convert_const.ValidFieldLabel.M_REPEATED)
    value = _check_get_get_field_value(col_schema.type, value_str, is_repeated)
    if value is None:
        raise RuntimeError(
            f'字段类型检查失败, 字段名: \'{col_schema.name}\', 字段类型: \'{col_schema.type}\', 字段label: \'{col_schema.label}\', 字段的值: {value_str}')

    if col_schema.ref is not None:
        # 替换引用的值
        value = reference_handler.replace_reference(col_schema, value)

    return value


def _check_get_get_field_value(field_type, value_str: str, is_repeated: bool) -> typing.Any:
    """
    检查并获取字段的值, 检查失败时返回None
    Args:
        field_type: eval过的字段类型
        value_str: [str]字符串处理过的单元格数据
        is_repeated: [bool]label是否为repeated
    Returns:
        真正的value的值
    """
    if is_repeated:
        # 可以填: 1|2|3
        value_list = value_str.split(genv.settings.repeated_value_splitter)
        if field_type == convert_const.ValidFieldType.BOOL:
            # 处理bool值乱填
            for idx, curr_value_str in enumerate(value_list):
                if curr_value_str.lower() == 'true':
                    value_list[idx] = 'True'
                if curr_value_str.lower() == 'false':
                    value_list[idx] = 'False'
        for idx, curr_value_str in enumerate(value_list):
            value = _check_get_get_field_value(field_type, curr_value_str, False)
            if value is None:
                return None
            value_list[idx] = value
        return value_list

    if field_type == convert_const.ValidFieldType.EVAL:
        value = eval(value_str)  # pylint: disable=eval-used
        return value

    if field_type == convert_const.ValidFieldType.LIST:
        value = eval(value_str)  # pylint: disable=eval-used
        if isinstance(value, list):
            return value
        if isinstance(value, tuple):
            # 也允许填成tuple
            return list(value)
        genv.logger.error('值应该是list或tuple类型, 然而填的值为: \'%s\'', value_str)
        return None

    if field_type == convert_const.ValidFieldType.DICT:
        value = eval(value_str)  # pylint: disable=eval-used
        if isinstance(value, dict):
            return value
        genv.logger.error('值应该是dict类型, 然而填的值为: \'%s\'', value_str)
        return None

    if field_type == convert_const.ValidFieldType.TIME:
        # 填秒，转为毫秒
        return int(float(value_str) * 1000.0)

    if field_type == convert_const.ValidFieldType.DATETIME:
        dt = datetime.datetime.strptime(value_str, '%Y-%m-%d %H:%M:%S')
        timestamp = time.mktime(dt.timetuple())
        return int(timestamp)

    if isinstance(field_type, type):
        # bool int float str
        if field_type == convert_const.ValidFieldType.BOOL:
            if value_str.lower() == 'true':
                return True
            if value_str.lower() == 'false':
                return False
            genv.logger.error('值应该为\'True\'或者\'False\', 然而填的值为: \'%s\'', value_str)
            return None
        if field_type == convert_const.ValidFieldType.INT:
            return int(value_str)
        if field_type == convert_const.ValidFieldType.FLOAT:
            return float(value_str)
        if field_type == convert_const.ValidFieldType.STR:
            value_str.replace('\r', '')
            value_str.replace('\n', '')
            return value_str

    genv.logger.error('暂时不支持字段类型: \'%s\', 值: \'%s\'', field_type, value_str)
    return None
