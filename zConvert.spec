# -*- mode: python -*-

block_cipher = None


a = Analysis(['zConvert_code.py'],
             pathex=['E:\\Zanweb\\PythonProgram\\Batch'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='zConvert_Beta',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
