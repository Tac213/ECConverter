# -*- mode: python ; coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

from PyInstaller.building.build_main import Analysis
from PyInstaller.building.api import PYZ, EXE, COLLECT
from PyInstaller.building.osx import BUNDLE

from const import app_const, path_const

import deploy_env  # pylint: disable=import-error

block_cipher = None

a = Analysis(
    deploy_env.scripts,
    pathex=deploy_env.pathex,
    binaries=[],
    datas=deploy_env.datas,
    hiddenimports=deploy_env.hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=app_const.APP_NAME,
    icon=path_const.APP_ICON_PATH if path_const.APP_ICON_PATH.endswith('.icns') else None,
    debug=deploy_env.deployment_args.variant == 'debug',
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=deploy_env.deployment_args.variant == 'debug',
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=app_const.APP_NAME,
)

app = BUNDLE(
    coll,
    name=f'{app_const.APP_NAME}.app',
    icon=path_const.APP_ICON_PATH if path_const.APP_ICON_PATH.endswith('.icns') else None,
    bundle_identifier=None,
)
