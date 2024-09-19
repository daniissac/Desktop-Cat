# -*- mode: python ; coding: utf-8 -*-

import sys
import PyInstaller.config

PyInstaller.config.CONF['distpath'] = "dist"
block_cipher = None

a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas=[('assets', 'assets')],  # Include the assets folder
             hiddenimports=['PyQt6'],
             hookspath=[],
             hooksconfig={},
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
          [],
          exclude_binaries=True,
          name='CatPet',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='CatPet')

# Create a .app bundle for macOS
if sys.platform == 'darwin':
    app = BUNDLE(coll,
                 name='CatPet.app',
                 icon=None,  # Replace with 'path/to/your/icon.icns' if you have an icon file
                 bundle_identifier='com.yourdomain.catpet',
                 info_plist={
                     'CFBundleName': 'Cat Pet',
                     'CFBundleDisplayName': 'Cat Pet',
                     'CFBundleGetInfoString': "Cat Pet Desktop Application",
                     'CFBundleVersion': "1.0.0",
                     'CFBundleShortVersionString': "1.0.0",
                     'NSHighResolutionCapable': True,
                     'NSRequiresAquaSystemAppearance': False,  # For dark mode support
                 })
