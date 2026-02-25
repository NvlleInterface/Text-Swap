# -*- mode: python ; coding: utf-8 -*-
import sys

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('shortcuts.json', '.'),
    ],
    hiddenimports=[
        'customtkinter',
        'pynput.keyboard',
        'pynput.mouse',
        'pystray',
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=['tkinter.test', 'unittest'],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='TextSwap',
    debug=False,
    strip=False,
    upx=True,
    console=False,
    windowed=True,
    icon='icon.ico' if sys.platform == 'win32' else None,
)
