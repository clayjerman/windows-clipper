# 🚀 GitHub CI/CD Guide - Automated Builds

## 📋 Overview

Dengan GitHub Actions, build aplikasi AI Clipper akan berjalan **otomatis** di cloud setiap kali Anda push new version, dan Anda bisa langsung download .exe yang sudah jadi!

**Benefits:**
- ✅ Tidak perlu install Rust di komputer Anda
- ✅ Build berjalan otomatis di GitHub servers
- ✅ Hasil build langsung tersedia untuk download
- ✅ Terintegrasi dengan GitHub Releases
- ✅ Gratis untuk public repositories

---

## 🎯 How It Works

```
You push tag → GitHub Actions starts → Build runs in cloud → .exe ready for download
     (v1.0.0)           (Automatic)             (10-20 min)          (Click & Download)
```

---

## 📝 Prerequisites

### 1. GitHub Repository
Punya repository GitHub untuk project ini.

**Jika belum ada:**
```bash
# Initialize git
cd D:\clipper
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - AI Clipper v1.0.0"

# Create GitHub repository
# Visit: https://github.com/new
# Then add remote:
git remote add origin https://github.com/YOUR_USERNAME/ai-clipper.git
git branch -M main
git push -u origin main
```

### 2. GitHub Token (Already Included)
GitHub Actions sudah memiliki `GITHUB_TOKEN` otomatis, tidak perlu setup manual.

### 3. Optional: Code Signing
Untuk menghindari warning "Windows protected your PC":
- Dapatkan code signing certificate (~$200/tahun)
- Upload ke GitHub Secrets
- Update workflow file untuk menggunakan certificate

**Ini opsional!** Bisa skip untuk MVP.

---

## 🔧 Setup Steps

### Step 1: Push Code to GitHub

```bash
cd D:\clipper

# Initialize git (jika belum)
git init

# Configure git (jika belum)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Add all files
git add .

# Commit
git commit -m "Initial commit - AI Clipper v1.0.0"

# Add remote (GANTI dengan URL repository Anda)
git remote add origin https://github.com/YOUR_USERNAME/ai-clipper.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 2: Verify Workflow File

Pastikan file workflow sudah ada:
```
.github/workflows/build.yml
```

File ini sudah dibuat otomatis oleh saya.

### Step 3: Trigger Build (Create Tag)

**Option A: Using Git Commands**
```bash
# Create version tag
git tag v1.0.0

# Push tag to GitHub
git push origin v1.0.0
```

**Option B: Using GitHub UI**
1. Buka repository GitHub Anda
2. Klik "Releases" → "Create a new release"
3. Tag: `v1.0.0`
4. Release title: `AI Clipper v1.0.0`
5. Klik "Publish release"

### Step 4: Wait for Build to Complete

1. Buka repository GitHub
2. Klik tab "Actions"
3. Lihat workflow "Build AI Clipper"
4. Tunggu sampai status berubah menjadi ✅ (sekitar 10-20 menit)

### Step 5: Download Installer

**Setelah build selesai:**

**Option A: From GitHub Releases**
1. Klik tab "Releases"
2. Klik release `v1.0.0`
3. Download: `AI-Clipper-v1.0.0-x64-setup.exe`

**Option B: From Actions Artifacts**
1. Klik tab "Actions"
2. Klik workflow run yang selesai
3. Scroll ke "Artifacts"
4. Download: `AI-Clipper-installer`

---

## 🎬 Complete Workflow Example

```bash
# 1. Make changes to code
cd D:\clipper
# Edit some files...

# 2. Commit changes
git add .
git commit -m "Fix bug in video processing"

# 3. Push to GitHub
git push

# 4. Create new version tag
git tag v1.0.1
git push origin v1.0.1

# 5. Wait 10-20 minutes...

# 6. Download from GitHub Releases!
```

---

## 🔍 What Happens During Build

GitHub Actions akan:

1. ✅ Setup Windows runner
2. ✅ Checkout your code
3. ✅ Setup Node.js (v18)
4. ✅ Setup Rust toolchain
5. ✅ Install FFmpeg
6. ✅ Install Python and dependencies
7. ✅ Build frontend
8. ✅ Build Tauri application
9. ✅ Create .exe installer
10. ✅ Upload to GitHub Releases

**Total time:** ~10-20 menit

---

## 📦 What Gets Built

**Installer:** `AI-Clipper-v1.0.0-x64-setup.exe`
- Size: ~150-300 MB
- Contains: Complete app with all dependencies
- Platform: Windows 10/11 (64-bit)

**Artifacts:** `AI-Clipper-installer.zip`
- Same installer, available for 90 days
- Downloadable from Actions tab

---

## 🔄 Version Management

### Creating New Releases

```bash
# Make changes
git add .
git commit -m "Add new features"

# Bump version
git tag v1.1.0
git push origin main
git push origin v1.1.0

# Build runs automatically!
```

### Versioning Strategy

- **v1.0.0** - Initial release
- **v1.0.1** - Bug fixes
- **v1.1.0** - New features
- **v2.0.0** - Major changes

---

## 🔐 Optional: Code Signing

Untuk menghindari warning "Windows protected your PC":

### Get a Certificate
Purchase from:
- DigiCert (~$200-500/year)
- Sectigo (~$100-300/year)
- GlobalSign (~$200-400/year)

### Setup GitHub Secrets

1. Go to GitHub repository → Settings → Secrets and variables → Actions
2. Add secret:
   - Name: `TAURI_PRIVATE_KEY`
   - Value: Your private key content

3. Add secret:
   - Name: `TAURI_KEY_PASSWORD`
   - Value: Your certificate password

### Update Workflow

Workflow file sudah mendukung code signing dengan secrets tersebut.

**Note:** Ini opsional! Tanpa code signing, user hanya akan melihat warning (bisa di-click "Run anyway").

---

## 🐛 Troubleshooting

### Issue: Build fails

**Check:**
1. Go to Actions tab
2. Click on failed workflow
3. Read error logs
4. Fix the issue
5. Commit and push again

### Issue: Workflow doesn't trigger

**Make sure:**
- [ ] Tag starts with `v` (e.g., `v1.0.0`)
- [ ] Tag is pushed to GitHub (`git push origin v1.0.0`)
- [ ] Workflow file is in `.github/workflows/build.yml`

### Issue: Download fails

**Try:**
1. Wait a few minutes after build completes
2. Refresh the page
3. Check if release is published (not draft)
4. Try downloading from Actions Artifacts instead

### Issue: Build takes too long

**Normal:** 10-20 minutes for first build
**Faster:** Subsequent builds may be faster with caching
**Very slow:** Check if there are errors in logs

---

## 💡 Best Practices

### 1. Test Before Release
```bash
# Test locally first (optional)
cd D:\clipper\frontend
npm run tauri:build
# If this works, push to GitHub
```

### 2. Use Descriptive Commit Messages
```bash
git commit -m "Fix: Improve video export speed"
git commit -m "Feat: Add TikTok subtitle style"
git commit -m "Docs: Update user guide"
```

### 3. Keep Releases Clean
```bash
# Don't push tags for every commit
# Only tag for actual releases
git tag v1.0.0  # ✅ Good
git tag wip     # ❌ Bad (not a version)
```

### 4. Monitor Build Status
- Enable email notifications for Actions
- Check Actions tab regularly
- Fix build failures quickly

---

## 📊 Build Time Breakdown

| Step | Time |
|------|------|
| Setup | 1-2 min |
| Install dependencies | 2-3 min |
| Build frontend | 1-2 min |
| Build Rust/Tauri | 5-10 min |
| Upload & Release | 1-2 min |
| **Total** | **10-20 min** |

---

## 🎯 Quick Reference

### Commands

```bash
# Push code
git push origin main

# Create release
git tag v1.0.0
git push origin v1.0.0

# View tags
git tag -l

# Delete tag (if needed)
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0
```

### URLs

- Actions: `https://github.com/YOUR_USERNAME/ai-clipper/actions`
- Releases: `https://github.com/YOUR_USERNAME/ai-clipper/releases`
- Latest Release: `https://github.com/YOUR_USERNAME/ai-clipper/releases/latest`

---

## 🎉 Summary

### What You Need to Do

1. **Push code to GitHub** (1x)
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/ai-clipper.git
   git push -u origin main
   ```

2. **Create tag for release** (each release)
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

3. **Wait 10-20 minutes**

4. **Download from GitHub Releases**

### What GitHub Does Automatically

- ✅ Sets up build environment
- ✅ Installs all dependencies
- ✅ Builds the application
- ✅ Creates .exe installer
- ✅ Publishes to Releases
- ✅ Makes it available for download

### What Users Get

- ✅ Ready-to-use .exe installer
- ✅ Double-click to install
- ✅ No technical setup needed
- ✅ Complete with all dependencies

---

## 📞 Support

If you encounter issues:

1. Check Actions logs in GitHub
2. Read error messages carefully
3. Search for similar issues
4. Ask in GitHub Issues

**Documentation:**
- GitHub Actions: https://docs.github.com/en/actions
- Tauri: https://tauri.app/v1/guides/building/

---

Made with ❤️ by the AI Clipper Team
**Build Automatically with GitHub Actions! 🚀**
