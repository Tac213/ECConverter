# -*- coding: utf-8 -*-
# author: Tac
# contact: gzzhanghuaxiong@corp.netease.com

from PyQt6.QtCore import QAbstractItemModel, QModelIndex, Qt
from PyQt6.QtGui import QIcon

from gui.model.excel_list_node import ExcelListNode


class ExcelListModel(QAbstractItemModel):
    """
    ListView的Model
    """

    def __init__(self, parent=None):
        """
        构造器
        Args:
            parent: 父Widget
        """
        super(ExcelListModel, self).__init__(parent)
        self.nodes = {}
        self.root = ExcelListNode('')

    def index(self, row, column, parent=QModelIndex()):
        """
        PyQt6的虚函数
        通过父节点索引获取子节点索引
        Args:
            row: [int]子节点行索引值
            column: [int]子节点列索引值
            parent: [QModelIndex]父节点索引
        Returns:
            QModelIndex
        """
        parent_node = parent.internalPointer() if parent.isValid() else self.root
        if row >= parent_node.children_count():
            return QModelIndex()
        return self.createIndex(row, column, parent_node.children[row])

    def parent(self, child):
        """
        PyQt6的虚函数
        通过子节点索引获取父节点索引
        Args:
            child: [QModelIndex]子节点索引
        Returns:
            QModelIndex
        """
        if not child.isValid():
            return QModelIndex()
        node = child.internalPointer()
        if node.parent is self.root:
            return QModelIndex()
        return self.createIndex(node.parent.row(), 0, node.parent)

    def rowCount(self, parent=QModelIndex()):
        """
        PyQt6的虚函数
        用于获取获取父节点下子节点的行数
        Args:
            parent: [QModelIndex]节点索引
        Returns:
            int
        """
        node = parent.internalPointer() if parent.isValid() else self.root
        return node.children_count()

    def columnCount(self, parent=QModelIndex()):
        """
        PyQt6的虚函数
        用于获取父节点下子节点列数
        Args:
            parent: [QModelIndex]节点索引
        Returns:
            int
        """
        return 1

    def flags(self, index):
        """
        PyQt6的虚函数
        用于获取节点Flag
        Args:
            index: [QModelIndex]节点索引
        Returns:
            Qt.ItemFlag
        """
        if not index.isValid():
            return
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

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
            return QIcon('res/excel.png')

    def add_node(self, parent_index, path):
        """
        增加一个节点
        Args:
            parent_index: [QModelIndex]父节点索引
            path: [str]Excel相对路径
        Returns:
            None
        """
        parent_node = parent_index.internalPointer() if parent_index.isValid() else self.root
        self.beginInsertRows(parent_index, parent_node.children_count(), parent_node.children_count())
        child = ExcelListNode(path, parent_node)
        parent_node.add_child(child)
        self.endInsertRows()

    def remove_node(self, index):
        """
        删除一个节点
        Args:
            index: [QModelIndex]节点索引
        Returns:
            None
        """
        if not index.isValid():
            return
        parent_index = index.parent()
        parent_node = index.internalPointer().parent
        self.beginRemoveRows(parent_index, index.internalPointer().row(), index.internalPointer().row())
        node = index.internalPointer()
        parent_node.remove_child(node.row())
        self.endRemoveRows()

    def serialize(self):
        """
        序列化，得到要导的Excel列表
        Returns:
            list，每一项是Excel的相对路径
        """
        data = []
        root_data = self.root.serialize()
        for child_data in root_data['children']:
            data.append(child_data['path'])
        return data

    def deserialize(self, data):
        """
        反序列化，重设整个list的数据
        Args:
            data: [list]数据，每一项是Excel的相对路径
        Returns:
            None
        """
        self.beginResetModel()

        self.root.clear_children()
        for path in data:
            child = ExcelListNode(path, self.root)
            self.root.add_child(child)

        self.endResetModel()
