# -*- mode: python ; coding: utf-8 -*-
"""
作家工厂（Writer Factory）PyInstaller 打包配置。

用法（在项目根目录 WriterFactory/ 下）：
    # 1. 先收集静态资源
    python manage.py collectstatic --noinput
    # 2. 打包
    pyinstaller WriterFactory.spec --clean --noconfirm

产物：dist/WriterFactory/WriterFactory.exe（onedir 模式，启动快、兼容性好）
"""
import sys
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# ---------------------------------------------------------------------------
# 隐式导入：Django 迁移、webview 后端、waitress 等均为动态导入，需显式收集
# ---------------------------------------------------------------------------
hiddenimports = []
hiddenimports += collect_submodules('core')          # 含 core.migrations.0001_initial
hiddenimports += collect_submodules('writer_factory')
hiddenimports += collect_submodules('webview')       # 含各平台 webview 后端
hiddenimports += ['waitress', 'waitress.tcp', 'waitress.threads']
# Windows Edge WebView2 后端依赖 pythonnet/clr
if sys.platform == 'win32':
    hiddenimports += ['clr', 'webview.platforms.edgechromium', 'webview.platforms.winforms']

# ---------------------------------------------------------------------------
# 数据文件：模板、静态资源、Django 内置 admin/认证模板与静态文件
# ---------------------------------------------------------------------------
datas = []
datas += collect_data_files('core')                  # core/templates、core/static
datas += collect_data_files('django')                # admin 模板/静态、locale
# collectstatic 生成的静态资源根目录（打包后由 STATIC_ROOT 提供服务）
datas += [('staticfiles', 'staticfiles')]

# 不需要的重型模块，减小体积
excludes = ['tkinter', 'matplotlib', 'numpy', 'pandas', 'PyQt5', 'PySide2']


a = Analysis(
    ['app_launcher.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='WriterFactory',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,           # 桌面应用不显示控制台
    disable_windowed_traceback=False,
    # icon='assets/app.ico',  # 如有图标可在此指定
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='WriterFactory',
)
