# -*- coding: utf-8 -*-
# author: Tac
# contact: gzzhanghuaxiong@corp.netease.com

from PyQt6.QtWidgets import QListView, QMenu
from PyQt6.QtCore import Qt


class ExcelListView(QListView):
    """
    ExcelList的View
    """

    def __init__(self, parent=None):
        """
        构造器
        Args:
            parent: 父Widget
        """
        super(ExcelListView, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        # self.setSizeAdjustPolicy(QListView.SizeAdjustPolicy.AdjustToContents)
        self.setSelectionMode(QListView.SelectionMode.ExtendedSelection)
        self.setDragDropMode(QListView.DragDropMode.NoDragDrop)
        self.setDragEnabled(False)
        self.setAcceptDrops(False)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._on_context_menu)
        self.menu = QMenu(self)
        remove_action = self.menu.addAction(self.tr('删除'))
        remove_action.triggered.connect(self._on_remove_node)

    def keyPressEvent(self, event):
        """
        重载KeyPressEvent，增加delete操作
        Args:
            event: QtGui.QKeyEvent
        Returns:
            None
        """
        if event.key() == Qt.Key.Key_Delete or event.key() == Qt.Key.Key_Backspace:
            self._on_remove_node()
        else:
            super(ExcelListView, self).keyPressEvent(event)

    def _on_context_menu(self, pos):
        """
        自定义右键菜单回调
        Args:
            pos: [QPoint]点的局部坐标
        Returns:
            None
        """
        if not self.selectedIndexes():
            return
        self.menu.exec(self.mapToGlobal(pos))

    def _on_remove_node(self):
        """
        移除节点动作回调
        Returns:
            None
        """
        indexes = self.selectedIndexes()
        for index in indexes:
            self.model().remove_node(index)
