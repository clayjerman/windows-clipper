# Quick Build & Distribution Guide

## 🚀 How to Build AI Clipper Installer

This guide will help you create a Windows installer (.exe) that anyone can install.

---

## 📋 Pre-Build Checklist

Before building, make sure:

- ✅ You have all the code files
- ✅ Icons are created in `frontend/src-tauri/icons/`
- ✅ Rust toolchain is installed
- ✅ Node.js and npm are working
- ✅ Application runs in development mode

---

## ⚡ Quick Start (5 Minutes)

### 1. Install Rust Toolchain (if not installed)

```powershell
# Download and run: https://rustup.rs/
# Or use PowerShell:
Invoke-WebRequest -Uri https://win.rustup.rs/x86_64 -OutFile rustup-init.exe
.\rustup-init.exe

# Choose option 1 (Default installation)
# Restart terminal after installation
```

### 2. Build the Application

```powershell
# Navigate to frontend folder
cd D:\clipper\frontend

# Install Tauri CLI (if not installed)
npm install -g @tauri-apps/cli

# Build the application (this takes 5-10 minutes)
npm run tauri:build
```

### 3. Find Your Installer

After building, the installer will be here:

```
D:\clipper\frontend\src-tauri\target\release\bundle\nsis\AI Clipper_1.0.0_x64-setup.exe
```

### 4. Test the Installer

```powershell
# Navigate to installer location
cd D:\clipper\frontend\src-tauri\target\release\bundle\nsis

# Run installer (double-click or use PowerShell)
.\AI Clipper_1.0.0_x64-setup.exe
```

---

## 📦 What Gets Created

After running `npm run tauri:build`, you'll get:

```
frontend/src-tauri/target/release/bundle/
├── msi/                    # MSI installer (Microsoft Installer)
│   └── AI Clipper_1.0.0_x64_en-US.msi
├── nsis/                   # NSIS installer (Recommended ⭐)
│   └── AI Clipper_1.0.0_x64-setup.exe  ← Use this one!
├── exe/                    # Portable executable (no installation needed)
│   └── AI Clipper.exe
└── wix/                    # WIX installer
    └── AI Clipper_1.0.0_x64_en-US.msi
```

**Recommended**: Use the NSIS installer (`AI Clipper_1.0.0_x64-setup.exe`)

---

## 🎯 Distribution Steps

### Step 1: Prepare Distribution Package

```powershell
# Create distribution folder
New-Item -ItemType Directory -Path "D:\clipper\dist" -Force

# Copy the main installer
Copy-Item "D:\clipper\frontend\src-tauri\target\release\bundle\nsis\*.exe" "D:\clipper\dist\"

# Copy documentation (optional but recommended)
Copy-Item "D:\clipper\docs\USER_GUIDE.md" "D:\clipper\dist\User Guide.md"
Copy-Item "D:\clipper\docs\TROUBLESHOOTING.md" "D:\clipper\dist\Troubleshooting.md"

# Create README for users
```

### Step 2: Create Distribution README

Create `D:\clipper\dist\README.txt`:

```
========================================
        AI Clipper v1.0.0
    AI-Powered Viral Clip Generator
========================================

INSTALLATION
============

1. Double-click: AI Clipper_1.0.0_x64-setup.exe
2. Click "Next" on the installer
3. Choose installation location (or use default)
4. Click "Install"
5. Click "Finish" to launch the app

SYSTEM REQUIREMENTS
===================

- Windows 10 or later (64-bit)
- 8 GB RAM minimum (16 GB recommended)
- 5 GB free disk space
- Internet connection (for YouTube and AI processing)

WHAT'S INCLUDED
===============

The installer includes everything you need:
- Built-in Python runtime (no Python installation needed)
- Built-in FFmpeg (for video processing)
- Built-in AI models (for transcription and analysis)
- Modern UI with dark theme

FIRST RUN
=========

1. Launch AI Clipper from Start Menu or Desktop
2. You'll be asked for a Gemini API key
3. Get your free key: https://makersuite.google.com/app/apikey
4. Enter the key and click "Continue"
5. You're ready to create viral clips!

HOW TO USE
==========

1. Paste a YouTube URL
2. Adjust settings (clip duration, number of clips, etc.)
3. Click "Generate Clips"
4. Wait for AI to process the video
5. Preview and edit the generated clips
6. Export clips as MP4 files (9:16 format)

SUPPORT
=======

Documentation included:
- User Guide.md - Detailed usage instructions
- Troubleshooting.md - Common issues and solutions

Website: https://aiclipper.dev
Email: support@aiclipper.dev

UNINSTALL
=========

To uninstall AI Clipper:
1. Go to Settings > Apps > Installed apps
2. Find "AI Clipper"
3. Click "..." and select "Uninstall"
4. Follow the uninstall wizard

Note: Uninstalling will remove the application but
preserve your project data and settings.

========================================
Made with ❤️ by the AI Clipper Team
Version 1.0.0 - Released 2024
========================================
```

### Step 3: Verify the Installer

Before distributing:

1. ✅ Test installer on a clean Windows machine
2. ✅ Verify all features work
3. ✅ Check file size (should be < 500MB)
4. ✅ Test uninstall process
5. ✅ Verify API key setup is clear

---

## 🌐 How to Distribute

### Option 1: GitHub Releases (Recommended - Free)

1. Create a GitHub repository (or use existing one)
2. Push your code to GitHub
3. Create a new release:
   ```powershell
   # Tag the version
   git tag v1.0.0
   git push origin v1.0.0
   ```
4. Go to GitHub → your repo → Releases → "Create a new release"
5. Enter release title and notes
6. Upload these files:
   - `AI Clipper_1.0.0_x64-setup.exe`
   - `README.txt`
   - `User Guide.md` (optional)
7. Click "Publish release"

Now users can download from:
```
https://github.com/yourusername/ai-clipper/releases/tag/v1.0.0
```

### Option 2: Direct Download from Website

1. Host the files on your website
2. Create a download page
3. Add these links:
   ```html
   <a href="downloads/AI-Clipper-1.0.0-setup.exe" download>
     Download AI Clipper v1.0.0
   </a>
   ```
4. Include checksum for security:
   ```powershell
   certutil -hashfile "AI Clipper_1.0.0_x64-setup.exe" SHA256
   ```

### Option 3: Cloud Storage

Upload to:
- Google Drive (share link)
- Dropbox (share link)
- OneDrive (share link)
- AWS S3 (public bucket)

---

## 🔐 Code Signing (Optional but Recommended)

Without code signing, Windows will show a security warning:

⚠️ "Windows protected your PC"

To avoid this, you need a code signing certificate.

### Self-Signed Certificate (Free but still shows warning)

```powershell
# Create self-signed certificate
New-SelfSignedCertificate `
  -Type CodeSigningCert `
  -Subject "CN=AI Clipper" `
  -CertStoreLocation "Cert:\LocalMachine\My"

# Export to PFX
$password = ConvertTo-SecureString "password123" -AsPlainText -Force
$cert = Get-ChildItem Cert:\LocalMachine\My | Where-Object { $_.Subject -eq "CN=AI Clipper" }
Export-PfxCertificate `
  -Cert $cert `
  -FilePath "aiclipper.pfx" `
  -Password $password
```

### Commercial Certificate (Recommended for public distribution)

Purchase from:
- DigiCert (~$200-$500/year)
- Sectigo (~$100-$300/year)
- GlobalSign (~$200-$400/year)

After getting certificate, sign the installer:

```powershell
signtool sign `
  /f aiclipper.pfx `
  /p password123 `
  /tr http://timestamp.digicert.com `
  /td sha256 `
  /fd sha256 `
  /d "AI Clipper" `
  "D:\clipper\frontend\src-tauri\target\release\bundle\nsis\AI Clipper_1.0.0_x64-setup.exe"
```

---

## 📊 File Size Information

Expected installer sizes:

- **NSIS Installer**: ~150-300 MB
- **MSI Installer**: ~150-300 MB
- **Portable EXE**: ~150-300 MB

Size breakdown:
- Frontend bundle: ~10 MB
- Tauri runtime: ~50 MB
- Python embedded: ~100 MB
- FFmpeg: ~30 MB
- AI models: ~50 MB

---

## 🎯 Quick Reference Commands

```powershell
# Build installer
cd D:\clipper\frontend
npm run tauri:build

# Find installer
cd D:\clipper\frontend\src-tauri\target\release\bundle\nsis
dir *.exe

# Test installer
.\AI Clipper_1.0.0_x64-setup.exe

# Create distribution package
cd D:\clipper
New-Item -ItemType Directory -Path "dist" -Force
Copy-Item "frontend\src-tauri\target\release\bundle\nsis\*.exe" "dist\"

# Create checksum
cd dist
certutil -hashfile "AI Clipper_1.0.0_x64-setup.exe" SHA256
```

---

## ❓ Common Issues

### Issue: Build fails with "cargo not found"

**Solution**: Install Rust toolchain
```powershell
# Download from https://rustup.rs/
# Or run:
Invoke-WebRequest -Uri https://win.rustup.rs/x86_64 -OutFile rustup-init.exe
.\rustup-init.exe
```

### Issue: Build takes too long

**Solution**: Build time is normal (5-10 minutes)
- Rust compilation is slow
- Only first build is slow
- Subsequent builds are faster with caching

### Issue: "Windows protected your PC" warning

**Solution**: Users need to click "More info" then "Run anyway"
- This is expected for unsigned apps
- Consider getting a code signing certificate for public distribution

### Issue: Icons not showing in installer

**Solution**: Make sure icons are in `frontend/src-tauri/icons/`:
- 32x32.png
- 128x128.png
- 128x128@2x.png
- icon.ico
- icon.icns

---

## 📞 Support

For build issues:
- Tauri Documentation: https://tauri.app/v1/guides/
- Rust Documentation: https://doc.rust-lang.org/
- GitHub Issues: https://github.com/tauri-apps/tauri/issues

---

## ✅ Success Checklist

Before distributing:

- [ ] Installer builds successfully
- [ ] Installer runs without errors
- [ ] Application installs correctly
- [ ] Application launches after installation
- [ ] All features work as expected
- [ ] API key setup is clear to users
- [ ] Error messages are user-friendly
- [ ] Uninstall process works
- [ ] File size is reasonable
- [ ] Documentation is included
- [ ] Tested on clean Windows machine

---

## 🎉 You're Ready!

Your AI Clipper application is now ready to distribute!

**Next Steps:**
1. Upload installer to GitHub Releases
2. Create download page on your website
3. Share with users
4. Collect feedback
5. Plan next version

---

Made with ❤️ by the AI Clipper Team
