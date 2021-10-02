# -*- coding: utf-8 -*-
# author: Tac
# contact: gzzhanghuaxiong@corp.netease.com

import os.path

from PyQt6.QtWidgets import QFrame, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy,\
    QFileDialog, QMessageBox, QCheckBox, QLabel
from PyQt6.QtCore import Qt, QDir, QModelIndex

from gui.excel_list_view import ExcelListView
from gui.model.enum_list_model import EnumListModel
import settings
import ec_converter


class SelectEnum(QFrame):
    """
    选择需要导出enum的窗口
    """

    def __init__(self, parent=None):
        """
        构造器
        Args:
            parent: 父Widget
        """
        super(SelectEnum, self).__init__(parent)
        self.enum_list_view = ExcelListView(self)
        model = EnumListModel()
        self.enum_list_view.setModel(model)
        self.data_validation_check_box = QCheckBox(self)
        self.data_validation_check_box.setChecked(True)  # 默认生成数据验证
        self.data_validation_check_box.setToolTip(self.tr('为引用enum的Excel的对应列增加数据验证'))
        self.data_validation_label = QLabel(self.tr('是否生成数据验证'), self)
        self.select_enum_button = QPushButton(self.tr('选择enum'), self)
        self.select_enum_button.setToolTip(self.tr('选择本次需要导出的enum目录，加到enum列表中'))
        self.select_enum_button.clicked.connect(self._on_select_enum)
        self.convert_button = QPushButton(self.tr('导出enum'), self)
        self.convert_button.setToolTip(self.tr('对enum列表中的所有enum目录执行导表程序'))
        self.convert_button.clicked.connect(self._on_convert)
        self.gen_info_button = QPushButton(self.tr('生成项目enum信息'), self)
        self.gen_info_button.setToolTip(self.tr('生成%s和%s') % (os.path.basename(settings.ENUM_INFO_FILENAME),
                                                              os.path.basename(settings.ENUM_REF_FILENAME)))
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
        layout.addWidget(self.enum_list_view)
        layout.addWidget(self.select_enum_button)
        convert_widget = QWidget()
        convert_layout = QHBoxLayout()
        convert_layout.addWidget(self.convert_button)
        convert_layout.addWidget(self.data_validation_check_box)
        convert_layout.addWidget(self.data_validation_label)
        convert_layout.setSpacing(10)
        convert_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        convert_widget.setLayout(convert_layout)
        convert_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout.addWidget(convert_widget)
        layout.addWidget(self.gen_info_button)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

    def set_enum_data(self, data):
        """
        设置要导出enum的数据
        Args:
            data: [list]数据，每一项是enum的相对路径
        Returns:
            None
        """
        self.enum_list_view.model().deserialize(data)

    def _on_select_enum(self):
        """
        点击“选择enum”按钮回调
        Returns:
            None
        """
        enum_path = QFileDialog.getExistingDirectory(
            self,
            self.tr('选择需要导出的enum'),
            self._excel_dir.path(),
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks,
        )
        if not enum_path:
            return
        current_enums = self.enum_list_view.model().serialize()
        enum_path = self._excel_dir.relativeFilePath(enum_path)
        if enum_path in current_enums:
            return
        if enum_path.startswith('..'):
            ec_converter.logger.warning(self.tr('所选enum目录必须要在\'%s\'目录内'), self._excel_dir.path())
            return
        if enum_path not in settings.ENUM_INFO:
            ec_converter.logger.warning(self.tr('所选enum目录必须要在这些目录内: \'%s\''), settings.ENUM_INFO.keys())
            return
        self.enum_list_view.model().add_node(QModelIndex(), enum_path)

    def _on_convert(self):
        """
        点击导出enum按钮回调
        Returns:
            None
        """
        import convert
        current_enums = self.enum_list_view.model().serialize()
        enums_full_path = []
        for enum in current_enums:
            full_path = self._excel_dir.absoluteFilePath(enum)
            enums_full_path.append(full_path)
        if enums_full_path:
            try:
                success = convert.convert_enum(enums_full_path, self.data_validation_check_box.isChecked())
                if success:
                    QMessageBox.information(self, self.tr('提示'), self.tr('导出enum成功'),
                                            QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
                else:
                    QMessageBox.critical(self, self.tr('错误'), self.tr('导出enum失败，失败原因请参照输出窗口'),
                                         QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            except Exception:
                stack_str = ec_converter.logger.log_last_except()
                QMessageBox.critical(self, self.tr('导出enum失败'), stack_str,
                                     QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)

    def _on_gen_info(self):
        """
        生成enum信息回调
        Returns:
            None
        """
        import convert
        try:
            success = convert.generate_enum_info()
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
