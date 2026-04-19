# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for the AI Clipper backend.

Build command (from project root):
    pyinstaller backend/backend.spec

Output:  dist/ai-clipper-backend.exe  (Windows)
         dist/ai-clipper-backend      (Linux / macOS)

After building, copy/rename the binary into the Tauri binaries folder:
    Windows : frontend/src-tauri/binaries/ai-clipper-backend-x86_64-pc-windows-msvc.exe
    Linux   : frontend/src-tauri/binaries/ai-clipper-backend-x86_64-unknown-linux-gnu
    macOS   : frontend/src-tauri/binaries/ai-clipper-backend-x86_64-apple-darwin
"""

block_cipher = None

a = Analysis(
    ["../run.py"],
    pathex=[".."],         # project root
    binaries=[],
    datas=[],
    hiddenimports=[
        # uvicorn internals not auto-detected
        "uvicorn.logging",
        "uvicorn.loops",
        "uvicorn.loops.auto",
        "uvicorn.loops.asyncio",
        "uvicorn.protocols",
        "uvicorn.protocols.http",
        "uvicorn.protocols.http.auto",
        "uvicorn.protocols.http.h11_impl",
        "uvicorn.protocols.websockets",
        "uvicorn.protocols.websockets.auto",
        "uvicorn.protocols.websockets.websockets_impl",
        "uvicorn.lifespan",
        "uvicorn.lifespan.off",
        "uvicorn.lifespan.on",
        # starlette / fastapi
        "starlette.routing",
        "starlette.middleware",
        "starlette.middleware.cors",
        "starlette.responses",
        "starlette.staticfiles",
        "fastapi",
        "fastapi.middleware.cors",
        # pydantic
        "pydantic",
        "pydantic.deprecated.class_validators",
        "pydantic_settings",
        # async / http
        "anyio",
        "anyio._backends._asyncio",
        "h11",
        "httptools",
        # backend package
        "backend",
        "backend.main",
        "backend.core.config",
        "backend.core.exceptions",
        "backend.models.video",
        "backend.models.clip",
        "backend.models.analysis",
        "backend.services.downloader",
        "backend.services.transcriber",
        "backend.services.analyzer",
        "backend.services.scorer",
        "backend.services.detector",
        "backend.services.editor",
        "backend.services.cache",
        "backend.utils.file_utils",
        "backend.utils.video_utils",
        "backend.utils.audio_utils",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        "matplotlib",
        "tkinter",
        "PyQt5",
        "PyQt6",
        "wx",
        "notebook",
        "IPython",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
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
    [],
    name="ai-clipper-backend",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,          # keep console so logs are visible / catchable by Tauri
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
