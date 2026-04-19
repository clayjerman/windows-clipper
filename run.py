"""
Backend entry point — used by both PyInstaller packaging and direct invocation.

    python run.py          # development
    ./ai-clipper-backend   # packaged
"""
import sys
import os

# Ensure the project root is on the path so 'backend' package is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=58174,
        log_level="info",
        reload=False,
    )
