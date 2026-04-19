# 🎬 AI Clipper - Generate Viral Short-Form Videos Automatically

<div align="center">

![AI Clipper](https://img.shields.io/badge/AI_Clipper-v1.0.0-blue)
![Platform](https://img.shields.io/badge/platform-Windows-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Production%20Ready-brightgreen)

**Transform YouTube videos into viral short-form content with AI**

[Features](#-features) • [Quick Start](#-quick-start) • [Installation](#-installation) • [Usage](#-usage) • [Download](#-download)

</div>

---

## 📋 Overview

**AI Clipper** is a professional-grade desktop application that automatically generates engaging short-form video clips from YouTube content. Perfect for content creators, marketers, and social media managers.

### ✨ Key Capabilities

- 🎥 **Download** videos from YouTube automatically
- 📝 **Transcribe** audio using Whisper AI
- 🧠 **Analyze** content with Gemini AI to find viral moments
- 👤 **Track** speakers and faces automatically
- ✂️ **Smart crop** videos to 9:16 vertical format
- 🎯 **Auto subtitles** with highlight effects
- 📱 **Export** ready-to-upload videos for TikTok, YouTube Shorts, Instagram Reels

### 🎯 Perfect For

- **Content Creators** - Repurpose long-form content
- **Marketers** - Create social media clips quickly
- **Influencers** - Maintain consistent posting schedule
- **Agencies** - Scale clip production for clients

---

## 🚀 Quick Start

### Option 1: Automated Build (Recommended - No Local Setup)

**You can get the .exe installer directly from GitHub Releases - no need to build yourself!**

1. Download installer from [GitHub Releases](https://github.com/YOUR_USERNAME/ai-clipper/releases)
2. Double-click `AI-Clipper-v1.0.0-x64-setup.exe`
3. Install application
4. Get free Gemini API key: https://makersuite.google.com/app/apikey
5. Paste YouTube URL and click "Generate Clips"
6. Done! 🎉

**Total time: 5 minutes**

---

## 💻 Installation

### System Requirements

- **OS:** Windows 10 or later (64-bit)
- **RAM:** 8 GB minimum (16 GB recommended)
- **Storage:** 5 GB free space
- **Internet:** Required for AI processing

### Download Options

#### 1. GitHub Releases (Easiest)

Download pre-built installer:
```
https://github.com/YOUR_USERNAME/ai-clipper/releases/latest
```

#### 2. Build from Source

See [BUILD_GUIDE.md](docs/BUILD_GUIDE.md) for detailed build instructions.

---

## 📖 Usage Guide

### Basic Workflow

```
1. Paste YouTube URL
2. Configure settings (duration, number of clips)
3. Click "Generate Clips"
4. Wait for AI processing (5-10 minutes)
5. Preview generated clips
6. Export selected clips
7. Upload to TikTok/Shorts/Reels!
```

### Step-by-Step

#### 1. Input Video URL

Paste any YouTube video URL:
- Standard: `https://www.youtube.com/watch?v=xxxxx`
- Short: `https://youtu.be/xxxxx`
- Supported: All YouTube video formats

#### 2. Configure Settings

- **Clip Duration:** 15-60 seconds
- **Number of Clips:** 1-10 clips
- **Subtitle Style:** Default, Bold, Pop, Minimal
- **Enhancements:**
  - ✅ Auto subtitles
  - ✅ Jump cuts
  - ✅ Speaker tracking

#### 3. Generate Clips

Click "Generate Clips" and wait for:
1. 📥 Download video (~1-2 min)
2. 📝 Transcribe audio (~2-3 min)
3. 🧠 Analyze content (~1-2 min)
4. 👤 Detect speakers (~1-2 min)
5. ✂️ Generate clips (~1-2 min)

**Total:** 5-10 minutes per video

#### 4. Preview & Select

- Preview each generated clip
- View viral score (0-100)
- Enable/disable clips for export
- Read AI-generated insights

#### 5. Export Videos

Export to:
- MP4 (H.264 codec)
- 1080x1920 (9:16 aspect ratio)
- Optimized for social media
- Ready to upload!

---

## 🎨 Features

### AI-Powered Analysis

#### 🧠 Content Analysis (Gemini)
- Detects emotional spikes
- Identifies viral phrases
- Finds engaging moments
- Ranks clips by virality score

#### 📝 Transcription (Whisper)
- High-accuracy speech-to-text
- Multiple language support
- Timestamp synchronization
- Keyword detection

#### 👤 Speaker Detection (MediaPipe)
- Face detection and tracking
- Mouth movement analysis
- Active speaker identification
- Smart focus (zoom on speaker)

### Video Processing

#### ✂️ Smart Editing
- Automatic clip extraction
- Jump cuts for pacing
- Scene change detection
- Smooth transitions

#### 📱 Format Conversion
- Horizontal to vertical (9:16)
- Smart cropping (focus on speaker)
- Resolution upscaling
- Bitrate optimization

#### 🎬 Effects
- Dynamic subtitles
- Key word highlights
- Zoom effects
- Speed adjustments

### User Interface

- 🌙 Modern dark theme
- 🎨 Clean, minimal design
- 🔄 Real-time progress
- 📊 Viral score visualization
- 🖼️ Clip thumbnails
- ⚡ Batch operations

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend (Tauri + React)              │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  UI Layout  │  │  Components  │  │   State Mgmt  │   │
│  └─────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────┘
                          ↕ WebSocket
┌─────────────────────────────────────────────────────────┐
│                  Backend (FastAPI + Python)              │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ API Routes  │  │   Services   │  │   Workers    │   │
│  └─────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────┘
                          ↕
┌─────────────────────────────────────────────────────────┐
│                     AI & Processing                       │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ Whisper     │  │  Gemini      │  │ MediaPipe    │   │
│  │ (Speech)    │  │  (Content)   │  │ (Vision)     │   │
│  └─────────────┘  └──────────────┘  └──────────────┘   │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ yt-dlp      │  │   FFmpeg     │  │   OpenCV     │   │
│  │ (Download)  │  │  (Editing)   │  │ (Processing) │   │
│  └─────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Tech Stack

- **Frontend:** React, TypeScript, Tauri, Tailwind CSS
- **Backend:** Python, FastAPI, WebSocket
- **AI:** Whisper (transcription), Gemini (analysis), MediaPipe (vision)
- **Video:** FFmpeg, yt-dlp, OpenCV
- **Build:** Cargo, Vite

---

## 📦 Build & Distribution

### Automated CI/CD (GitHub Actions)

Build automatically on GitHub - no local setup required!

```bash
# 1. Push code to GitHub
git push origin main

# 2. Create release tag
git tag v1.0.0
git push origin v1.0.0

# 3. Wait 10-20 minutes

# 4. Download from GitHub Releases!
```

**See [docs/AUTOMATED_BUILD_GUIDE.md](docs/AUTOMATED_BUILD_GUIDE.md)**

### Local Build

Build on your machine:

```bash
cd D:\clipper\frontend
npm run tauri:build
```

**See [docs/BUILD_GUIDE.md](docs/BUILD_GUIDE.md)**

---

## 📚 Documentation

### User Guides
- [USER_GUIDE.md](docs/USER_GUIDE.md) - Complete user manual
- [QUICK_START.md](docs/QUICK_START.md) - Get started in 5 minutes

### Developer Guides
- [BUILD_GUIDE.md](docs/BUILD_GUIDE.md) - Build instructions
- [AUTOMATED_BUILD_GUIDE.md](docs/AUTOMATED_BUILD_GUIDE.md) - GitHub CI/CD
- [API_REFERENCE.md](docs/API_REFERENCE.md) - API documentation

### Architecture
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - System design
- [PROGRESS.md](docs/PROGRESS.md) - Development status

---

## 🗺️ Roadmap

### v1.0 (Current)
- ✅ YouTube download
- ✅ Whisper transcription
- ✅ Gemini analysis
- ✅ Speaker tracking
- ✅ Smart cropping
- ✅ Auto subtitles
- ✅ Export to 9:16

### v1.1 (Planned)
- ⏳ TikTok direct upload
- ⏳ Instagram direct upload
- ⏳ YouTube Shorts direct upload
- ⏳ Custom subtitle styles
- ⏳ Background music library

### v2.0 (Future)
- ⏳ Batch processing (multiple videos)
- ⏳ AI voiceover generation
- ⏳ Advanced effects library
- ⏳ Cloud rendering option
- ⏳ Team collaboration

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

- This tool is for educational and personal use
- Respect copyright and YouTube's Terms of Service
- Generated clips are your responsibility
- Always review content before publishing

---

## 📞 Support

### Documentation
- [FAQ](docs/FAQ.md) - Common questions
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Known issues

### Community
- GitHub Issues - Bug reports and feature requests
- Discussions - Community chat and questions

### Contact
- Email: support@example.com
- Twitter: @aiclipper

---

## 🙏 Acknowledgments

- **Whisper** - OpenAI for speech recognition
- **Gemini** - Google for content analysis
- **MediaPipe** - Google for computer vision
- **Tauri** - Cross-platform framework
- **FFmpeg** - Video processing
- **yt-dlp** - YouTube downloader

---

## 📊 Stats

<div align="center">

![GitHub Stars](https://img.shields.io/github/stars/YOUR_USERNAME/ai-clipper?style=social)
![GitHub Forks](https://img.shields.io/github/forks/YOUR_USERNAME/ai-clipper?style=social)
![GitHub Issues](https://img.shields.io/github/issues/YOUR_USERNAME/ai-clipper)
![GitHub License](https://img.shields.io/github/license/YOUR_USERNAME/ai-clipper)

**Made with ❤️ by the AI Clipper Team**

[⬆ Back to Top](#-ai-clipper--generate-viral-short-form-videos-automatically)

</div>
