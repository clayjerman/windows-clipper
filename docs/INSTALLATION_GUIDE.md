# Installation Guide - AI Clipper

## System Requirements

### Minimum Requirements
- **OS**: Windows 10 or later (64-bit)
- **RAM**: 8 GB (16 GB recommended)
- **Storage**: 5 GB free space (more for large videos)
- **CPU**: Multi-core processor (Intel i5 / AMD Ryzen 5 or better)
- **GPU**: Optional (NVIDIA GPU recommended for faster Whisper transcription)

### Required Software

1. **Python 3.9 or later**
   - Download: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"
   - Verify: `python --version`

2. **Node.js 18 or later**
   - Download: https://nodejs.org/
   - Choose LTS version
   - Verify: `node --version`

3. **FFmpeg** (Required for video processing)
   - See FFmpeg Installation section below

---

## Quick Installation

### Option 1: Automated Installation (Recommended)

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd ai-clipper
   ```

2. **Install FFmpeg**
   - Right-click on `install_ffmpeg.ps1`
   - Select "Run with PowerShell"
   - Or run as Administrator in PowerShell:
     ```powershell
     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
     .\install_ffmpeg.ps1
     ```

3. **Install Python Dependencies**
   ```bash
   cd backend
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Install Frontend Dependencies**
   ```bash
   cd ../frontend
   npm install
   ```

5. **Configure API Keys**
   - Copy `.env.example` to `.env`
   - Add your Gemini API key:
     ```env
     GEMINI_API_KEY=your_actual_api_key_here
     ```
   - Get API key from: https://makersuite.google.com/app/apikey

6. **Run the Application**
   - Terminal 1 (Backend):
     ```bash
     cd backend
     venv\Scripts\activate
     uvicorn main:app --reload
     ```
   - Terminal 2 (Frontend):
     ```bash
     cd frontend
     npm run tauri:dev
     ```

### Option 2: Manual Installation

#### Step 1: Install FFmpeg

**Windows:**

1. Download FFmpeg from https://ffmpeg.org/download.html#build-windows
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to system PATH:
   - Right-click "This PC" → Properties
   - Advanced system settings → Environment Variables
   - Edit "Path" variable
   - Add `C:\ffmpeg\bin`
4. Verify: `ffmpeg -version`

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

#### Step 2: Python Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 3: Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

#### Step 4: Configuration

```bash
# Copy example config
cp .env.example .env

# Edit .env and add your API key
# GEMINI_API_KEY=your_actual_api_key_here
```

---

## Verifying Installation

### 1. Verify FFmpeg
```bash
ffmpeg -version
```
Expected: FFmpeg version information

### 2. Verify Python Environment
```bash
cd backend
venv\Scripts\activate
python --version
```
Expected: Python 3.9+

### 3. Verify Backend Dependencies
```bash
python -c "import fastapi; import yt_dlp; import whisper; print('Dependencies OK')"
```
Expected: "Dependencies OK"

### 4. Verify Frontend Dependencies
```bash
cd frontend
npm --version
node --version
```
Expected: Node.js 18+, npm 9+

### 5. Test Backend Server
```bash
cd backend
venv\Scripts\activate
uvicorn main:app --reload
```
Visit http://127.0.0.1:8000/docs to see API documentation

### 6. Test Frontend Dev Server
```bash
cd frontend
npm run dev
```
Visit http://localhost:1420 to see the application

---

## Troubleshooting

### FFmpeg Not Found

**Error**: `'ffmpeg' is not recognized...`

**Solution**:
1. Ensure FFmpeg is installed
2. Add FFmpeg to system PATH
3. Restart terminal/computer
4. Run `where ffmpeg` to verify

### Python Virtual Environment Issues

**Error**: Scripts not found or import errors

**Solution**:
```bash
# Delete old venv
rm -rf venv

# Create new venv
python -m venv venv

# Activate and reinstall
venv\Scripts\activate
pip install -r requirements.txt
```

### Whisper Model Download Fails

**Error**: Failed to load Whisper model

**Solution**:
1. Check internet connection
2. Try smaller model: `WHISPER_MODEL=tiny` in .env
3. Model will download on first use (takes ~100MB-1GB)

### Node.js Version Too Old

**Error**: Node.js version not supported

**Solution**:
1. Download Node.js 18+ from nodejs.org
2. Uninstall old version
3. Install new version
4. Verify: `node --version`

### Port Already in Use

**Error**: Address already in use (8000 or 1420)

**Solution**:
```bash
# Find process using port
netstat -ano | findstr :8000

# Kill process (replace PID with actual ID)
taskkill /PID <PID> /F

# Or use different port in .env:
PORT=8001
```

### TypeScript Compilation Errors

**Error**: Type errors in frontend

**Solution**:
```bash
cd frontend
npm install --save-dev @types/node
npm run type-check
```

### Tauri Build Fails

**Error**: Rust/Cargo not found

**Solution**:
```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Or download from https://rustup.rs/

# Verify
cargo --version
```

---

## Advanced Installation

### Using GPU for Whisper

If you have an NVIDIA GPU:

1. Install CUDA Toolkit: https://developer.nvidia.com/cuda-downloads
2. Install cuDNN: https://developer.nvidia.com/cudnn
3. Update .env:
   ```env
   WHISPER_DEVICE=cuda
   ```

### Production Deployment

For production builds:

1. **Build Backend**:
   ```bash
   cd backend
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

2. **Build Frontend**:
   ```bash
   cd frontend
   npm run build
   npm run tauri:build
   ```

3. **Docker Deployment** (optional):
   ```bash
   docker build -t ai-clipper .
   docker run -p 8000:8000 ai-clipper
   ```

---

## Updating

### Update Backend
```bash
cd backend
venv\Scripts\activate
git pull
pip install -r requirements.txt --upgrade
```

### Update Frontend
```bash
cd frontend
git pull
npm install
npm run tauri:build
```

---

## Uninstallation

### Remove Backend
```bash
cd backend
# Deactivate venv (if active)
deactivate
# Delete venv
rm -rf venv
```

### Remove Frontend
```bash
cd frontend
rm -rf node_modules
rm -rf dist
```

### Remove FFmpeg
```bash
# Delete installation folder
rm -rf C:\ffmpeg

# Remove from PATH
# Windows: Remove C:\ffmpeg\bin from Environment Variables
```

### Remove Application Data
```bash
# Delete data directory
rm -rf data
```

---

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Search [GitHub Issues](https://github.com/your-repo/issues)
3. Contact support: support@aiclipper.dev

---

## Next Steps

After installation:

1. Read the [User Guide](USER_GUIDE.md)
2. Check out the [API Reference](API_REFERENCE.md)
3. Start using AI Clipper!
