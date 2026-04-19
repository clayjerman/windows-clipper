# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for the AI Clipper backend — one-folder mode.

Build command (from project root):
    pyinstaller backend/backend.spec

Output folder: dist-backend/ai-clipper-backend/
  Copy that entire folder to frontend/src-tauri/backend-dist/ai-clipper-backend/
  before running the Tauri build.
"""

block_cipher = None

a = Analysis(
    ["../run.py"],
    pathex=[".."],
    binaries=[],
    datas=[],
    hiddenimports=[
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
        "starlette.routing",
        "starlette.middleware",
        "starlette.middleware.cors",
        "starlette.responses",
        "starlette.staticfiles",
        "fastapi",
        "fastapi.middleware.cors",
        "pydantic",
        "pydantic.deprecated.class_validators",
        "pydantic_settings",
        "anyio",
        "anyio._backends._asyncio",
        "h11",
        "httptools",
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

# One-folder EXE — no extraction on every launch
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="ai-clipper-backend",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="ai-clipper-backend",
)
