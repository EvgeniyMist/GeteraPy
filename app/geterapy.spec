# -*- mode: python ; coding: utf-8 -*-

from os import path


block_cipher = None

a = Analysis(['..\\src\\main.py', '..\\src\\labs.py', '..\\src\\wbase.py', '..\\src\\rbase.py'],
             pathex=[path.abspath(SPECPATH)],
             binaries=[],
             datas=[('..\\data\\4x4 matrices.txt', '.'), ('..\\data\\5x5 matrices.txt', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='geterapy',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir='.',
          console=True )
