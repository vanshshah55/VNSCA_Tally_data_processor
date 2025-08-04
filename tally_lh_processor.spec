# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# List of all Python files in the project
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['pandas._libs.tslibs.timedeltas', 'pandas._libs.tslibs.nattype', 'pandas._libs.tslibs.np_datetime', 'pandas._libs.skiplist'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'scipy', 'PyQt5', 'PyQt6', 'PySide2', 'PySide6', 'IPython', 'notebook', 'sphinx', 'pytest', 'test'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Exclude unnecessary pandas modules to reduce size
a.binaries = [x for x in a.binaries if not x[0].startswith('pandas/tests/')]
a.binaries = [x for x in a.binaries if not x[0].startswith('pandas/io/formats/templates/')]
a.binaries = [x for x in a.binaries if not x[0].startswith('pandas/io/excel/_')]

# Exclude unnecessary numpy modules to reduce size
a.binaries = [x for x in a.binaries if not x[0].startswith('numpy/core/tests/')]
a.binaries = [x for x in a.binaries if not x[0].startswith('numpy/doc/')]
a.binaries = [x for x in a.binaries if not x[0].startswith('numpy/f2py/')]
a.binaries = [x for x in a.binaries if not x[0].startswith('numpy/testing/')]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Tally_LH_Processor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='tally_lh_processor.ico',
    version='file_version_info.txt',
)