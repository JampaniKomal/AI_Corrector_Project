# -*- mode: python ; coding: utf-8 -*-

# Complete AI Corrector Installer - Bundles EVERYTHING
# Installer + Uninstaller + Main App (204MB) in ONE .exe

import os
from pathlib import Path

# Base paths
installer_dir = Path(SPECPATH)
project_root = installer_dir.parent
dist_dir = project_root / 'dist'
assets_dir = project_root / 'assets'

# Files to bundle
datas = []

# Bundle the main application executable
main_exe = dist_dir / 'AICorrector.exe'
if main_exe.exists():
    datas.append((str(main_exe), 'dist'))
    print(f"✓ Bundling main app: {main_exe.name}")
else:
    print(f"⚠ WARNING: Main app not found at {main_exe}")

# Bundle assets (icons, logos)
if assets_dir.exists():
    datas.append((str(assets_dir), 'assets'))
    print(f"✓ Bundling assets folder")

# Bundle uninstaller script
uninstaller_script = installer_dir / 'uninstaller_ui.py'
if uninstaller_script.exists():
    datas.append((str(uninstaller_script), '.'))
    print(f"✓ Bundling uninstaller")

a = Analysis(
    ['installer_ui.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'win32com.client',
        'win32com.shell',
        'pywintypes',
        'pythoncom',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'IPython',
        'jupyter',
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AICorrector-Setup-v2.3.0',
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
    icon=str(assets_dir / 'app_logo.ico') if (assets_dir / 'app_logo.ico').exists() else None,
)

print("\n" + "="*60)
print("COMPLETE INSTALLER BUILD CONFIGURATION")
print("="*60)
print(f"Output: AICorrector-Setup-v2.3.0.exe")
print(f"Expected size: ~240 MB (33 MB installer + 204 MB app + assets)")
print("Contains: Installer + Uninstaller + Main App")
print("="*60)
