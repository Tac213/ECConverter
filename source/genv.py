# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import os

from const import path_const, app_const
import settings as settings_module
from log import logger as logger_module
from log import log_manager

logger = None  # type: logger_module.Logger
settings = None  # type: settings_module.ECConverterSettings


def initialize() -> None:
    _init_logger()
    _init_settings()


def _init_logger() -> None:
    global logger
    if not os.path.isdir(path_const.LOG_DIR):
        os.mkdir(path_const.LOG_DIR)
    log_manager.LogManager.set_tag(app_const.APP_NAME)
    logger = log_manager.LogManager.get_logger(app_const.APP_NAME, save_file=True, dirname=path_const.LOG_DIR)
    log_manager.LogManager.setup_std_logger()


def _init_settings() -> None:
    global settings
    settings = settings_module.initialize_settings()


def finalize() -> None:
    pass
