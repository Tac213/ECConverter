# -*- coding: utf-8 -*-
# This file is generated automatically by: ECConverter
# Raw excel directory name: example_enum
# Do not modify this file manually
# Your modification will be overridden when the automatic generation is performed
# Unless you know what you are doing


class GameGlobalEvent(object):
    """
    游戏全局事件
    """
    ENTER_LOGIN_SCENE = 1  # 进入登录场景
    ENTER_COMBAT_SCENE = 2  # 进入战斗场景


class SceneId(object):
    """
    各场景id
    """
    LOGIN_SCENE = 'LoginScene'  # 登录场景
    COMBAT_SCENE = 'CombatScene'  # 战斗场景


class BTreeNodeState(object):
    """
    行为树节点的状态
    """
    FAILURE = 0  # 失败
    SUCCESS = 1  # 成功
    RUNNING = 2  # 运行中
    BREAK = 3  # 运行中被打断
