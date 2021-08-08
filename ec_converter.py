# -*- coding: utf-8 -*-
# author: Tac
# contact: gzzhanghuaxiong@corp.netease.com

import sys
import os

import const
import dependency
import settings
import log_manager


logger = None


def _init_logger():
    """
    初始化logger
    Returns:
        None
    """
    global logger
    log_dir_path = os.path.abspath(const.LOG_DIR_NAME)
    # 创建log目录
    if not os.path.exists(log_dir_path):
        os.mkdir(log_dir_path)
    log_manager.LogManager.tag = const.LOGGER_NAME
    logger = log_manager.LogManager.get_logger(const.LOGGER_NAME, save_file=True, dirname=const.LOG_DIR_NAME)
    log_manager.LogManager.set_handler(log_manager.STREAM)


def main():
    """
    主函数，打开应用窗口
    Returns:
        None
    """
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtGui import QIcon
    from gui.main_window import MainWindow

    app = QApplication(sys.argv)

    # 设置应用基础信息
    app.setApplicationName(const.APP_NAME)
    app.setApplicationDisplayName(const.APP_NAME)
    app.setDesktopFileName(const.APP_NAME)
    app.setWindowIcon(QIcon(const.APP_ICON))

    # 显示主窗口, 如果不用一个变量勾住这个窗口的实例，这个窗口将无法被显示出来，即使在类里面写self.show()也没用
    main_window = MainWindow()
    main_window.on_window_ready()
    main_window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    dependency.check_dependency()
    settings.read_config()
    main()
else:
    # 要在__main__外面初始化logger，否则外部模块拿不到logger
    # 而且__main__的时候也不要初始化logger
    _init_logger()
