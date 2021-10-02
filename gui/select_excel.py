# -*- coding: utf-8 -*-
# author: Tac
# contact: gzzhanghuaxiong@corp.netease.com

import os.path

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QSizePolicy, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt, QDir, QModelIndex

from gui.excel_list_view import ExcelListView
from gui.model.excel_list_model import ExcelListModel
import settings
import ec_converter


class SelectExcel(QFrame):
    """
    选择需要导出Excel的窗口
    """

    def __init__(self, parent=None):
        """
        构造器
        Args:
            parent: 父Widget
        """
        super(SelectExcel, self).__init__(parent)
        self.excel_list_view = ExcelListView(self)
        model = ExcelListModel()
        self.excel_list_view.setModel(model)
        self.select_excel_button = QPushButton(self.tr('选择Excel'), self)
        self.select_excel_button.setToolTip(self.tr('选择本次需要导表的Excel文件，加到Excel列表中'))
        self.select_excel_button.clicked.connect(self._on_select_excel)
        self.convert_button = QPushButton(self.tr('导表'), self)
        self.convert_button.setToolTip(self.tr('对Excel列表中的所有Excel文件执行导表程序'))
        self.convert_button.clicked.connect(self._on_convert)
        self.gen_info_button = QPushButton(self.tr('生成项目Excel信息'), self)
        self.gen_info_button.setToolTip(self.tr('生成%s和%s') % (os.path.basename(settings.EXCEL_INFO_FILENAME),
                                                              os.path.basename(settings.REF_FILENAME)))
        self.gen_info_button.clicked.connect(self._on_gen_info)
        self._excel_dir = QDir(settings.EXCEL_DIR)
        self._init_layout()

    def _init_layout(self):
        """
        初始化layout
        Returns:
            None
        """
        layout = QVBoxLayout()
        layout.addWidget(self.excel_list_view)
        layout.addWidget(self.select_excel_button)
        layout.addWidget(self.convert_button)
        layout.addWidget(self.gen_info_button)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

    def set_excel_data(self, data):
        """
        设置要导出Excel的数据
        Args:
            data: [list]数据，每一项是Excel的相对路径
        Returns:
            None
        """
        self.excel_list_view.model().deserialize(data)

    def _on_select_excel(self):
        """
        点击“选择Excel”按钮回调
        Returns:
            None
        """
        # _是fileter，这里没有用
        files, _ = QFileDialog.getOpenFileNames(
            self,
            self.tr('选择需要导表的Excel'),
            self._excel_dir.path(),
            '*.xlsx',
        )
        current_files = self.excel_list_view.model().serialize()
        for file_path in files:
            file_path = self._excel_dir.relativeFilePath(file_path)
            if file_path in current_files:
                continue
            if file_path.startswith('..'):
                ec_converter.logger.warning(self.tr('所选Excel文件必须要在\'%s\'目录内'), self._excel_dir.path())
                continue
            if '/' in file_path:
                ec_converter.logger.warning(self.tr('所选Excel文件不能在\'%s\'目录的子目录内'), self._excel_dir.path())
                continue
            self.excel_list_view.model().add_node(QModelIndex(), file_path)

    def _on_convert(self):
        """
        点击导表按钮回调
        Returns:
            None
        """
        import convert
        current_files = self.excel_list_view.model().serialize()
        files_full_path = []
        for file in current_files:
            full_path = self._excel_dir.absoluteFilePath(file)
            files_full_path.append(full_path)
        if files_full_path:
            try:
                success = convert.convert_data(files_full_path)
                if success:
                    QMessageBox.information(self, self.tr('提示'), self.tr('导表成功'),
                                            QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
                else:
                    QMessageBox.critical(self, self.tr('错误'), self.tr('导表失败，失败原因请参照输出窗口'),
                                         QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            except Exception:
                stack_str = ec_converter.logger.log_last_except()
                QMessageBox.critical(self, self.tr('导表失败'), stack_str,
                                     QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)

    def _on_gen_info(self):
        """
        生成表格信息回调
        Returns:
            None
        """
        import convert
        try:
            success = convert.generate_excel_info()
            if success:
                QMessageBox.information(self, self.tr('提示'), self.tr('生成成功'),
                                        QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            else:
                QMessageBox.critical(self, self.tr('错误'), self.tr('生成失败，失败原因请参照输出窗口'),
                                     QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
        except Exception:
            stack_str = ec_converter.logger.log_last_except()
            QMessageBox.critical(self, self.tr('生成失败'), stack_str,
                                 QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
