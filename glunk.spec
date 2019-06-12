# -*- mode: python -*-

block_cipher = None


a = Analysis(['4dchess.py'],
             pathex=['C:\\Users\\anona\\Desktop\\4D-chess'],
             binaries=[],
             datas=[('C:\\Users\\anona\\AppData\\Local\\Programs\\Python\\Python36\\Lib\\site-packages\\vpython', 'vpython')],
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
          [],
          exclude_binaries=True,
          name='glunk',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='glunk')
