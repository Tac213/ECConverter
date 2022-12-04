# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import os
from urllib import parse
from PySide6 import QtCore, QtQml

# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)
QML_IMPORT_NAME = 'Python.FileIOHelper'
QML_IMPORT_MAJOR_VERSION = 1
QML_IMPORT_MINOR_VERSION = 0


@QtQml.QmlElement
class FileIOHelper(QtCore.QObject):

    @QtCore.Slot(str, str, result=str)
    def read_text_file(self, file_url, encoding) -> str:
        file_path = self.get_file_path_from_url(file_url)
        if not os.path.exists(file_path):
            return ''
        with open(file_path, 'r', encoding=encoding) as fp:
            content = fp.read()
        return content

    @QtCore.Slot(str, str, str)
    def write_text_file(self, file_url, encoding, content) -> None:
        file_path = self.get_file_path_from_url(file_url)
        with open(file_path, 'w', encoding=encoding) as fp:
            fp.write(content)

    @classmethod
    def get_file_path_from_url(cls, file_url: str) -> str:
        parse_result = parse.urlparse(file_url)
        return parse_result.path[1:] if parse_result.path.startswith('/') else parse_result.path
