# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import typing

from PySide6 import QtCore, QtQml

from model import item_list_node

# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)
QML_IMPORT_NAME = 'Python.ItemListModel'
QML_IMPORT_MAJOR_VERSION = 1
QML_IMPORT_MINOR_VERSION = 0


@QtQml.QmlElement
class ItemListModel(QtCore.QAbstractItemModel):
    """
    ListView的Model
    """

    path_role = QtCore.Qt.ItemDataRole.UserRole + 1

    def __init__(self, parent=None):
        """
        构造器
        Args:
            parent: 父object
        """
        super().__init__(parent)
        self.nodes = {}
        self.root = item_list_node.ItemListNode('')

    def index(self, row, column, parent=QtCore.QModelIndex()) -> QtCore.QModelIndex:
        """
        Qt的虚函数
        通过父节点索引获取子节点索引
        Args:
            row: [int]子节点行索引值
            column: [int]子节点列索引值
            parent: [QModelIndex]父节点索引
        Returns:
            QModelIndex
        """
        parent_node = parent.internal_pointer() if parent.is_valid() else self.root
        if row >= parent_node.children_count() or row < 0:
            return QtCore.QModelIndex()
        return self.create_index(row, column, parent_node.children[row])

    def parent(self, child: QtCore.QModelIndex) -> QtCore.QModelIndex:
        """
        Qt的虚函数
        通过子节点索引获取父节点索引
        Args:
            child: [QModelIndex]子节点索引
        Returns:
            QModelIndex
        """
        if not child.is_valid():
            return QtCore.QModelIndex()
        node = child.internal_pointer()  # type: item_list_node.ItemListNode
        if node.parent is self.root:
            return QtCore.QModelIndex()
        return self.create_index(node.parent.row(), 0, node.parent)

    def row_count(self, parent=QtCore.QModelIndex()) -> int:
        """
        Qt的虚函数
        用于获取获取父节点下子节点的行数
        Args:
            parent: [QModelIndex]节点索引
        Returns:
            int
        """
        node = parent.internal_pointer() if parent.is_valid() else self.root
        return node.children_count()

    def column_count(self, parent=QtCore.QModelIndex()) -> int:
        """
        Qt的虚函数
        用于获取父节点下子节点列数
        Args:
            parent: [QModelIndex]节点索引
        Returns:
            int
        """
        return 1

    def flags(self, index) -> QtCore.Qt.ItemFlag:
        """
        Qt的虚函数
        用于获取节点Flag
        Args:
            index: [QModelIndex]节点索引
        Returns:
            Qt.ItemFlag
        """
        if not index.is_valid():
            return
        return QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable

    def data(self, index: QtCore.QModelIndex, role: QtCore.Qt.ItemDataRole):
        """
        Qt的虚函数
        用于获取节点数据
        Args:
            index: [QModelIndex]节点索引
            role: Qt.ItemDataRole
        Returns:
            节点数据
        """
        if not index.is_valid():
            return
        node = index.internal_pointer()  # type: item_list_node.ItemListNode
        if role == self.path_role:
            return node.path

    def role_names(self) -> typing.Dict[QtCore.Qt.ItemDataRole, QtCore.QByteArray]:
        """
        Qt的虚函数
        返回qml可以用的变量名以及对应的role
        """
        return {
            self.path_role: QtCore.QByteArray(b'path'),
        }

    @QtCore.Slot(QtCore.QModelIndex, str)
    def add_node(self, parent_index: QtCore.QModelIndex, path: str) -> None:
        """
        增加一个节点
        Args:
            parent_index: [QModelIndex]父节点索引
            path: [str]Excel相对路径
        Returns:
            None
        """
        parent_node = parent_index.internal_pointer() if parent_index.is_valid() else self.root
        self.begin_insert_rows(parent_index, parent_node.children_count(), parent_node.children_count())
        child = item_list_node.ItemListNode(path, parent_node)
        parent_node.add_child(child)
        self.end_insert_rows()

    @QtCore.Slot(QtCore.QModelIndex)
    def remove_node(self, index: QtCore.QModelIndex) -> None:
        """
        删除一个节点
        Args:
            index: [QModelIndex]节点索引
        Returns:
            None
        """
        if not index.is_valid():
            return
        parent_index = index.parent()
        node = index.internal_pointer()  # type: item_list_node.ItemListNode
        parent_node = node.parent
        self.begin_remove_rows(parent_index, node.row(), node.row())
        parent_node.remove_child(node.row())
        self.end_remove_rows()

    @QtCore.Slot(result=list)
    def serialize(self):
        """
        序列化, 得到要导的Excel列表
        Returns:
            list, 每一项是Excel的相对路径
        """
        data = []
        root_data = self.root.serialize()
        for child_data in root_data['children']:
            data.append(child_data['path'])
        return data

    @QtCore.Slot(list)
    def deserialize(self, data: typing.List[str]):
        """
        反序列化, 重设整个list的数据
        Args:
            data: [list]数据, 每一项是Excel的相对路径
        Returns:
            None
        """
        self.begin_reset_model()

        self.root.clear_children()
        for path in data:
            child = item_list_node.ItemListNode(path, self.root)
            self.root.add_child(child)

        self.end_reset_model()
