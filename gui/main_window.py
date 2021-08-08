# -*- coding: utf-8 -*-
# author: Tac
# contact: gzzhanghuaxiong@corp.netease.com

import os.path
import json

from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget

from gui.select_excel import SelectExcel
from gui.output_window import OutputWindow
import ec_converter
import const

main_window = None  # MainWindow的实例


class MainWindow(QMainWindow):
    """
    gui界面的主窗口
    """

    def __init__(self, parent=None):
        """
        构造器
        Args:
            parent: 父Widget
        """
        super(MainWindow, self).__init__(parent)
        self.select_excel_widget = SelectExcel(self)
        self.output_window = OutputWindow(self)

        self._setup_ui()
        global main_window
        main_window = self

    def _setup_ui(self):
        """
        setup界面
        Returns:
            None
        """
        self.resize(800, 400)
        # 根据上一次选择的excel打开界面
        pref_filename = os.path.abspath(const.PREFERENCE_FILENAME)
        if os.path.exists(pref_filename):
            with open(pref_filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data['remember_last_excels']:
                    self.select_excel_widget.set_excel_data(data['last_excels'])
        central_widget = QWidget(self)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.select_excel_widget)
        layout.addWidget(self.output_window)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def on_window_ready(self):
        """
        main window准备完成回调
        Returns:
            None
        """
        from log_manager import OutputWindowHandler
        OutputWindowHandler.main_window_ready = True
        ec_converter.logger.info(self.tr('第一步：选择需要导表的Excel'))
        ec_converter.logger.info(self.tr('第二步：点击导表按钮，开始导表'))

    def closeEvent(self, _):
        """
        应用关闭回调
        记录上一次保存的信息
        Args:
            _: [QtGui.QCloseEvent]关闭事件，可以调accept/ignore等，这里暂时用不到
        Returns:
            None
        """
        with open(os.path.abspath(const.PREFERENCE_FILENAME), 'w', encoding='utf-8') as f:
            data = {
                'remember_last_excels': True,
                'last_excels': self.select_excel_widget.excel_list_view.model().serialize()
            }
            f.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ':')))
