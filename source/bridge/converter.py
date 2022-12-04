# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import typing

from PySide6 import QtCore, QtQml

import convert

# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)
QML_IMPORT_NAME = 'Python.Converter'
QML_IMPORT_MAJOR_VERSION = 1
QML_IMPORT_MINOR_VERSION = 0


@QtQml.QmlElement
class Converter(QtCore.QObject):

    @QtCore.Slot(list, result=bool)
    def convert_data(self, file_list: typing.List[str]) -> bool:
        return convert.convert_data(file_list)

    @QtCore.Slot(list, bool, result=bool)
    def convert_enum(self, enum_list: typing.List[str], is_set_data_validation: bool) -> bool:
        return convert.convert_enum(enum_list, is_set_data_validation)

    @QtCore.Slot(result=bool)
    def generate_excel_info(self) -> bool:
        return convert.generate_excel_info()

    @QtCore.Slot(result=bool)
    def generate_enum_info(self) -> bool:
        return convert.generate_enum_info()
