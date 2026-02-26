# -*- mode: python ; coding: utf-8 -*-
import sys

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('theme_retro.json', '.'),
        ('textswap-icon.png', '.'),
    ],
    hiddenimports=[
        'customtkinter',
        'pynput.keyboard',
        'pynput.mouse',
        'pystray',
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
        'PIL.ImageTk',
        'plyer',
        'plyer.platforms',
        'plyer.platforms.win.notification',
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
    icon='textswap-icon.ico',
)
