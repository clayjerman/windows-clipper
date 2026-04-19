# Build & Distribution Guide - AI Clipper

## 📋 Prerequisites

Before building, ensure:
- ✅ FFmpeg is installed and added to PATH
- ✅ All dependencies are installed
- ✅ Application works in development mode
- ✅ Node.js 18+ is installed
- ✅ Rust toolchain is installed
- ✅ Python 3.9+ is installed (for backend)

---

## 🏗️ Building Strategy

### Option 1: Tauri Standalone (Recommended)
Frontend + Rust backend bundled as single .exe
**Pros**: No Python needed on user machine, easy installation
**Cons**: Backend needs to be rewritten in Rust (time-consuming)

### Option 2: Tauri + Embedded Python
Frontend (Tauri) + Backend (Python embedded)
**Pros**: Backend code already written, faster to build
**Cons**: Larger download size (~500MB), includes Python runtime

### Option 3: Separate Installers
Frontend installer + Backend installer
**Pros**: Smaller downloads, modular
**Cons**: Two installation steps for users

### Option 4: Portable Version
Single folder with all dependencies
**Pros**: No installation needed, portable
**Cons**: Very large size (~1GB), slower startup

**We'll use Option 2: Tauri + Embedded Python** for best balance.

---

## 🔧 Step-by-Step Build Process

### Step 1: Install Rust Toolchain

If not already installed:

```powershell
# Download rustup-init.exe from https://rustup.rs/
# Or run (requires PowerShell):
Invoke-WebRequest -Uri https://win.rustup.rs/x86_64 -OutFile rustup-init.exe
.\rustup-init.exe

# Select option 1 (Default installation)
# Restart terminal after installation

# Verify installation
rustc --version
cargo --version
```

### Step 2: Install Tauri CLI

```powershell
cd D:\clipper\frontend
npm install -g @tauri-apps/cli

# Verify
tauri --version
```

### Step 3: Prepare for Build

#### 3.1 Update Tauri Configuration

Edit `frontend/src-tauri/tauri.conf.json`:

```json
{
  "build": {
    "beforeBuildCommand": "npm run build",
    "distDir": "../dist"
  },
  "bundle": {
    "active": true,
    "targets": ["msi", "nsis"],  // Windows installers
    "icon": ["icons/icon.ico"],
    "identifier": "com.aiclipper.app",
    "category": "Productivity",
    "shortDescription": "AI-powered viral clip generator",
    "longDescription": "Generate engaging short-form clips from YouTube videos using AI"
  }
}
```

#### 3.2 Create App Icons

You need icons in these sizes:

```
frontend/src-tauri/icons/
├── 32x32.png
├── 128x128.png
├── 128x128@2x.png
├── icon.icns (macOS)
└── icon.ico (Windows)
```

**Quick icon generation:**

Option 1: Use online tool
- Visit https://realfavicongenerator.net/
- Upload your logo (512x512 PNG)
- Download and extract
- Copy icons to `frontend/src-tauri/icons/`

Option 2: Create simple icons (for testing):
```powershell
# Create placeholder icon
# You'll need a real logo for production
```

### Step 4: Build Frontend

```powershell
cd D:\clipper\frontend
npm run build
```

This creates a `dist/` folder with optimized production build.

### Step 5: Build Tauri App

```powershell
cd D:\clipper\frontend
npm run tauri:build
```

This will take several minutes and will:
- Build Rust backend
- Bundle frontend assets
- Create Windows installers

**Expected output locations:**
```
frontend/src-tauri/target/release/bundle/
├── msi/                    # MSI installer
│   └── AI Clipper_1.0.0_x64_en-US.msi
├── nsis/                   # NSIS installer
│   └── AI Clipper_1.0.0_x64-setup.exe
├── exe/                    # Portable executable
│   └── AI Clipper.exe
└── wix/                    # WIX installer
    └── AI Clipper_1.0.0_x64_en-US.msi
```

### Step 6: Test the Installer

```powershell
# Test NSIS installer (recommended)
cd D:\clipper\frontend\src-tauri\target\release\bundle\nsis
.\AI Clipper_1.0.0_x64-setup.exe

# Test portable version
cd D:\clipper\frontend\src-tauri\target\release\bundle\exe
.\AI Clipper.exe
```

---

## 📦 Distribution Package

### Create Distribution Folder

```powershell
# Create distribution folder
New-Item -ItemType Directory -Path "D:\clipper\dist" -Force

# Copy installers
Copy-Item "D:\clipper\frontend\src-tauri\target\release\bundle\nsis\*.exe" "D:\clipper\dist\"
Copy-Item "D:\clipper\frontend\src-tauri\target\release\bundle\msi\*.msi" "D:\clipper\dist\"

# Copy documentation
Copy-Item "D:\clipper\docs\USER_GUIDE.md" "D:\clipper\dist\"
Copy-Item "D:\clipper\docs\INSTALLATION_GUIDE.md" "D:\clipper\dist\"

# Create README for distribution
```

### Create Distribution README

Create `D:\clipper\dist\README.txt`:

```
========================================
        AI Clipper v1.0.0
    AI-Powered Viral Clip Generator
========================================

INSTALLATION
============

Option 1: Recommended Installer (NSIS)
--------------------------------------
1. Double-click: AI Clipper_1.0.0_x64-setup.exe
2. Follow the installation wizard
3. Launch from Start Menu or Desktop

Option 2: MSI Installer
-----------------------
1. Double-click: AI Clipper_1.0.0_x64_en-US.msi
2. Follow the installation wizard
3. Launch from Start Menu

REQUIREMENTS
============

- Windows 10 or later (64-bit)
- 8 GB RAM minimum (16 GB recommended)
- 5 GB free disk space
- Internet connection (for AI processing)

SYSTEM REQUIREMENTS
===================

The application includes everything you need:
- Built-in Python runtime
- Built-in FFmpeg
- Built-in AI models

No additional installation required!

FIRST RUN
=========

1. Launch AI Clipper
2. You'll be prompted for a Gemini API key
3. Get your free key: https://makersuite.google.com/app/apikey
4. Enter the key and click "Continue"
5. You're ready to use AI Clipper!

SUPPORT
=======

Documentation:
- USER_GUIDE.md - How to use the application
- INSTALLATION_GUIDE.md - Troubleshooting

Website: https://aiclipper.dev
Email: support@aiclipper.dev

UPDATES
=======

The application will check for updates automatically.
You can also check manually from the Help menu.

UNINSTALL
=========

To uninstall:

Option 1:
1. Go to Control Panel > Programs and Features
2. Find "AI Clipper"
3. Click Uninstall

Option 2:
1. Run the installer again
2. Select "Remove" option

Note: This will remove the application but preserve
your project data and settings.

========================================
Made with ❤️ by the AI Clipper Team
Version 1.0.0 - Released 2024
========================================
```

### Create Version Info File

Create `D:\clipper\dist\VERSION.txt`:

```
AI Clipper
Version: 1.0.0
Release Date: 2024-04-15
Build Number: 2024.04.15.001

Changelog:
- Initial release
- YouTube video download
- AI-powered transcription (Whisper)
- Content analysis (Gemini)
- Viral moment detection
- Smart auto-cropping
- Subtitle generation
- Export to MP4 (9:16 format)

Known Issues:
- None reported

Minimum Requirements:
- Windows 10 64-bit
- 8 GB RAM
- 5 GB disk space
- Internet connection
```

---

## 🚀 Alternative: PyInstaller (Python Backend Only)

If you want to create a .exe without Tauri:

### Install PyInstaller

```powershell
cd D:\clipper\backend
venv\Scripts\activate
pip install pyinstaller
```

### Create Build Script

Create `D:\clipper\backend\build_app.spec`:

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['D:\\clipper\\backend'],
    binaries=[],
    datas=[
        ('data', 'data'),
    ],
    hiddenimports=[
        'fastapi',
        'uvicorn',
        'yt_dlp',
        'whisper',
        'google.generativeai',
        'mediapipe',
        'cv2',
        'numpy',
        'PIL',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='AI Clipper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='path/to/icon.ico',
)
```

### Build

```powershell
cd D:\clipper\backend
venv\Scripts\activate
pyinstaller build_app.spec
```

---

## 📋 Pre-Distribution Checklist

Before distributing to others:

- [ ] Application builds successfully
- [ ] Installer runs without errors
- [ ] Application launches correctly after installation
- [ ] All features work end-to-end
- [ ] API key setup is clear to users
- [ ] Error messages are user-friendly
- [ ] Documentation is included
- [ ] Icons and branding are correct
- [ ] File size is reasonable (< 500MB)
- [ ] Tested on clean Windows machine
- [ ] Antivirus scanning passes
- [ ] License and terms are included

---

## 🌐 Distribution Methods

### Option 1: GitHub Releases (Free)

1. Create GitHub repository
2. Tag release: `git tag v1.0.0`
3. Push tag: `git push origin v1.0.0`
4. Go to GitHub → Releases → Create release
5. Upload files:
   - `AI Clipper_1.0.0_x64-setup.exe`
   - `AI Clipper_1.0.0_x64_en-US.msi`
   - `README.txt`
   - `VERSION.txt`
6. Add release notes
7. Publish

### Option 2: Website Download

1. Host on your website:
   ```
   https://aiclipper.dev/download
   ```
2. Provide direct download links
3. Include hash verification:
   ```powershell
   certutil -hashfile "AI Clipper_1.0.0_x64-setup.exe" SHA256
   ```

### Option 3: Cloud Storage

- Google Drive
- Dropbox
- AWS S3
- Cloudflare R2

### Option 4: App Stores (Future)

- Microsoft Store (requires certification)
- Steam (for games/tools)
- Third-party software distribution

---

## 🔐 Code Signing (Optional but Recommended)

### Self-Signed Certificate

```powershell
# Create self-signed certificate
New-SelfSignedCertificate `
  -Type CodeSigningCert `
  -Subject "CN=AI Clipper" `
  -CertStoreLocation "Cert:\LocalMachine\My"

# Export to .pfx
$password = ConvertTo-SecureString "password123" -AsPlainText -Force
Export-PfxCertificate `
  -Cert (Get-ChildItem Cert:\LocalMachine\My\* -Subject "CN=AI Clipper")[0] `
  -FilePath "aiclipper.pfx" `
  -Password $password
```

### Sign the Executable

```powershell
# Sign the executable
signtool sign `
  /f aiclipper.pfx `
  /p password123 `
  /t http://timestamp.digicert.com `
  /d "AI Clipper" `
  "D:\clipper\frontend\src-tauri\target\release\bundle\exe\AI Clipper.exe"
```

### Commercial Certificate

For professional distribution:
- DigiCert: https://www.digicert.com/
- Sectigo: https://sectigo.com/
- GlobalSign: https://www.globalsign.com/

Cost: ~$200-$500/year

---

## 📊 File Size Optimization

### Reduce Size

```powershell
# 1. Use UPX compression (already enabled in Tauri)
# 2. Exclude unnecessary Python packages
# 3. Minimize static assets
# 4. Use optimized images
```

### Split into Components

```
ai-clipper-core.exe (50 MB)   - Main app
ai-clipper-models.zip (300 MB) - AI models (download on first run)
ai-clipper-data.zip (100 MB)  - Required data files
```

---

## 🎯 Quick Build Command Reference

```powershell
# Full build (frontend + installer)
cd D:\clipper\frontend
npm run build
npm run tauri:build

# Quick rebuild (no frontend)
cd D:\clipper\frontend\src-tauri
cargo build --release

# Create distribution package
cd D:\clipper
Copy-Item frontend\src-tauri\target\release\bundle\nsis\*.exe dist\
Copy-Item docs\*.md dist\
```

---

## ✅ Final Steps

1. **Build**: Run `npm run tauri:build`
2. **Test**: Install on clean Windows machine
3. **Package**: Copy installers to `dist/` folder
4. **Document**: Include README and user guide
5. **Distribute**: Upload to GitHub Releases
6. **Monitor**: Track downloads and issues

---

## 📞 Support

For build issues:
- Tauri Docs: https://tauri.app/v1/guides/
- PyInstaller Docs: https://pyinstaller.org/
- GitHub Issues: https://github.com/your-repo/issues

---

Made with ❤️ by the AI Clipper Team
