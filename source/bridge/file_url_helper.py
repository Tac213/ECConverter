# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

from PySide6 import QtCore, QtQml
from __feature__ import snake_case, true_property  # pylint: disable=import-error,unused-import

from const import path_const
import genv

# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)
QML_IMPORT_NAME = 'Python.FileUrlHelper'
QML_IMPORT_MAJOR_VERSION = 1
QML_IMPORT_MINOR_VERSION = 0


@QtQml.QmlElement
class FileUrlHelper(QtCore.QObject):

    @QtCore.Slot(result=str)
    def root_dir(self) -> str:
        return QtCore.QUrl.from_local_file(path_const.ROOT_PATH).to_string()

    @QtCore.Slot(result=str)
    def excel_dir(self) -> str:
        return QtCore.QUrl.from_local_file(genv.settings.excel_dir).to_string()
