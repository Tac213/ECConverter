# -*- coding: utf-8 -*-
# author: Tac
# contact: gzzhanghuaxiong@corp.netease.com

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from gui.model.excel_list_model import ExcelListModel


class EnumListModel(ExcelListModel):
    """
    enum的ListView的model
    """

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        """
        PyQt6的虚函数
        用于获取节点数据
        Args:
            index: [QModelIndex]节点索引
            role: Qt.ItemDataRole
        Returns:
            节点数据
        """
        if not index.isValid():
            return
        node = index.internalPointer()
        if role == Qt.ItemDataRole.DisplayRole:
            return node.path
        if role == Qt.ItemDataRole.DecorationRole:
            return QIcon('res/opened_folder.png')
