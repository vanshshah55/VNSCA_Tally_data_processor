# -*- mode: python ; coding: utf-8 -*-

# This is an optimized spec file for a SINGLE-FILE executable.

block_cipher = None

# --- Aggressive Excludes to reduce size ---
excludes = [
    'matplotlib', 'scipy', 'PyQt5', 'PyQt6', 'PySide2', 'PySide6',
    'IPython', 'notebook', 'jupyter_client', 'jupyter_core', 'qtconsole', 'zmq',
    'sphinx', 'pytest', 'test', 'tests', 'pandas.tests', 'numpy.tests',
    'tkinter.test', 'tkinter.tix'
]

# --- Hidden Imports for pandas ---
hiddenimports = [
    'pandas._libs.tslibs.timedeltas',
    'pandas._libs.tslibs.nattype',
    'pandas._libs.tslibs.np_datetime',
    'pandas._libs.skiplist'
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('tally_lh_processor.ico', '.')],
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Tally_LH_Processor_Optimized',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=False,  # This creates a windowed application
    icon='tally_lh_processor.ico'
)
