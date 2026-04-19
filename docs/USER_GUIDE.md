# 📖 AI Clipper User Guide

## 🚀 Quick Start

### Installation

1. Download the installer from [GitHub Releases](https://github.com/YOUR_USERNAME/ai-clipper/releases)
2. Double-click `AI-Clipper-v1.0.0-x64-setup.exe`
3. Follow the installation wizard
4. Launch AI Clipper from Start Menu

### First-Time Setup

When you first launch AI Clipper, you'll be prompted to set up your API keys:

1. **Gemini API Key** (Required)
   - Get free key from: https://makersuite.google.com/app/apikey
   - Paste the key in the setup screen
   - Click "Save & Continue"

2. **OpenAI API Key** (Optional)
   - Get key from: https://platform.openai.com/api-keys
   - Add in Settings later if needed

For detailed instructions, see [API Key Setup Guide](API_KEY_SETUP_GUIDE.md)

---

## 📋 Interface Overview

### Main Layout

```
┌─────────────────────────────────────────────────────────┐
│  AI Clipper Logo                    [Settings]          │
├──────────────┬──────────────────────────┬───────────────┤
│              │                          │               │
│   Left       │       Center              │    Right      │
│   Panel      │       Panel               │    Panel      │
│              │                          │               │
│  • URL Input │  • Video Player           │  • Clip List  │
│  • Settings  │  • Progress Bar           │  • Export     │
│  • Generate  │  • Selected Clip Info     │  • Selection  │
│              │                          │               │
└──────────────┴──────────────────────────┴───────────────┘
```

### Left Panel
- **URL Input:** Paste YouTube video URL
- **Settings:** Configure clip duration, number, etc.
- **Generate Button:** Start processing

### Center Panel
- **Video Preview:** Watch original video
- **Progress Bar:** Track processing status
- **Selected Clip Info:** View clip details

### Right Panel
- **Clip List:** View all generated clips
- **Selection:** Choose clips to export
- **Export:** Download selected clips

---

## 🎬 Creating Your First Clip

### Step 1: Enter YouTube URL

1. Find a YouTube video you want to clip
2. Copy the video URL
3. Paste it in the URL input field
4. Wait for validation (green checkmark appears)

### Step 2: Configure Settings

**Clip Duration:** 15-60 seconds
- **15-30s:** Best for TikTok
- **30-60s:** Best for YouTube Shorts
- **45-90s:** Best for Instagram Reels

**Number of Clips:** 1-10 clips
- More clips = more options
- Recommended: 3-5 clips

**Subtitle Style:**
- Default: Clean, modern subtitles
- Bold: Large, bold text
- Pop: Colorful, animated
- Minimal: Minimalist design

**Enhancements:**
- ✅ Auto Subtitles: Generate captions automatically
- ✅ Jump Cuts: Remove silence for faster pacing

### Step 3: Generate Clips

1. Click **Generate Clips** button
2. Wait for processing (5-10 minutes)

**Processing Stages:**
1. 📥 Downloading video (~1-2 min)
2. 📝 Transcribing audio (~2-3 min)
3. 🧠 Analyzing content (~1-2 min)
4. 👤 Detecting speakers (~1-2 min)
5. ✂️ Generating clips (~1-2 min)

**Progress Bar:** Shows current stage and percentage

### Step 4: Preview and Select

Once processing is complete:

1. **View Clips:** All generated clips appear in the Right Panel
2. **Preview:** Click any clip to preview
3. **Check Scores:** View viral score (0-100)
4. **Read Insights:** AI-generated insights for each clip
5. **Select Clips:** Click checkbox to select for export

**Viral Score:**
- **90+:** Excellent (highly viral)
- **70-89:** Good (good potential)
- **Below 70:** Fair (consider re-editing)

### Step 5: Export Clips

1. Select clips you want to export (or select all)
2. Click **Export** button
3. Choose output location
4. Wait for export to complete
5. Find exported clips in your chosen folder

**Export Format:**
- **File Type:** MP4 (H.264)
- **Resolution:** 1080x1920 (9:16 vertical)
- **Quality:** HD
- **Ready for:** TikTok, YouTube Shorts, Instagram Reels

---

## ⚙️ Settings

### Access Settings

1. Click **Settings** button in top-right corner
2. Configure options
3. Click **Save** to apply changes

### API Keys

**Gemini API Key** (Required)
- Required for AI features
- Get from: https://makersuite.google.com/app/apikey
- Enter in Settings or during setup

**OpenAI API Key** (Optional)
- For additional AI features
- Get from: https://platform.openai.com/api-keys
- Optional, not required for basic use

**Managing Keys:**
- **Test Key:** Verify key is working
- **Save:** Update keys
- **Clear:** Remove all keys

### Other Settings

- **Theme:** Dark/Light mode
- **Auto-save:** Automatically save projects
- **Default Clip Duration:** Set preferred duration
- **Default Number of Clips:** Set preferred count

---

## 📱 Export Options

### Export Selected Clips

1. Select clips using checkboxes
2. Click **Export** button
3. Wait for export to complete

### Export All Clips

1. Click **Select All** checkbox
2. Click **Export** button
3. Wait for export to complete

### After Export

Exported clips are ready to upload:
- **TikTok:** Upload directly or use TikTok Studio
- **YouTube Shorts:** Upload via YouTube Studio
- **Instagram Reels:** Upload via Instagram app or studio

---

## 💡 Tips for Best Results

### Choosing Videos

✅ **Good Videos:**
- High quality (720p+)
- Clear speech (good for transcription)
- Engaging content
- Multiple speakers
- Emotional moments

❌ **Avoid:**
- Low quality videos
- Poor audio
- Long silences
- Monotone content
- No clear structure

### Optimizing Settings

**For TikTok:**
- Duration: 15-30 seconds
- Number: 3-5 clips
- Subtitles: Essential
- Jump cuts: Recommended

**For YouTube Shorts:**
- Duration: 30-60 seconds
- Number: 2-4 clips
- Quality: 1080p
- Hook: First 3 seconds crucial

**For Instagram Reels:**
- Duration: 30-90 seconds
- Number: 2-3 clips
- Music: Add in Instagram
- Trending: Use trending audio

### Improving Viral Scores

- **Choose videos with emotional content**
- **Look for controversial or surprising moments**
- **Select clips with clear hooks**
- **Ensure good audio quality**
- **Optimize for your target audience**

---

## 🔍 Understanding AI Analysis

### Viral Score (0-100)

AI analyzes multiple factors:

1. **Emotional Intensity** (20%)
   - Voice pitch variation
   - Emotional spikes
   - Engaging moments

2. **Keyword Relevance** (25%)
   - Viral phrases
   - Trending topics
   - Engaging words

3. **Speaker Engagement** (25%)
   - Active speaking time
   - Energy level
   - Face expressions

4. **Pacing** (15%)
   - Fast-paced moments
   - Jump cut opportunities
   - Dynamic transitions

5. **Scene Changes** (15%)
   - Visual interest
   - Camera movement
   - Background changes

### Clip Insights

Each clip includes AI-generated insights:
- **Summary:** What the clip is about
- **Key Points:** Main topics covered
- **Viral Potential:** Why it might go viral
- **Suggestions:** How to improve

---

## 🎯 Advanced Features

### Batch Processing

Process multiple videos sequentially:
1. Process first video
2. Export clips
3. Start next video
4. Repeat

### Custom Clip Editing

Select specific timestamps:
1. Preview video
2. Mark start/end points
3. Generate custom clip
4. Export

### Subtitle Customization

After export, you can:
- Edit subtitle text
- Change subtitle style
- Adjust timing
- Add translations

---

## 📊 Performance Optimization

### Faster Processing

**Hardware:**
- Use SSD storage
- 16 GB+ RAM
- Multi-core CPU
- Dedicated GPU (optional)

**Settings:**
- Reduce number of clips
- Shorter clip duration
- Disable jump cuts

### Reducing Costs

**Free Tier (Gemini):**
- 1,500 requests/day
- Process ~10-20 videos/day

**Tips:**
- Process fewer videos
- Generate fewer clips
- Use free tier efficiently

---

## ❓ Troubleshooting

### Common Issues

**Issue: "Invalid URL"**
- ✅ Ensure it's a valid YouTube URL
- ✅ Use share link from YouTube
- ✅ Check for typos

**Issue: "Download Failed"**
- ✅ Check internet connection
- ✅ Try a different video
- ✅ Some videos may be restricted

**Issue: "API Key Required"**
- ✅ Add Gemini API key in Settings
- ✅ Get key from: https://makersuite.google.com/app/apikey
- ✅ Restart application

**Issue: "Export Failed"**
- ✅ Check disk space
- ✅ Choose different output location
- ✅ Close other applications

**Issue: "Processing Too Slow"**
- ✅ Close other applications
- ✅ Use SSD storage
- ✅ Reduce number of clips
- ✅ Shorten clip duration

For more troubleshooting, see [Troubleshooting Guide](TROUBLESHOOTING.md)

---

## 📚 Additional Resources

### Documentation
- [API Key Setup Guide](API_KEY_SETUP_GUIDE.md)
- [FAQ](FAQ.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [API Reference](API_REFERENCE.md)

### External Resources
- [Gemini Documentation](https://ai.google.dev/docs)
- [YouTube Terms of Service](https://www.youtube.com/t/terms)

---

## 🎓 Tutorials

### Tutorial 1: Create Your First TikTok Clip

**Video:** [Watch Tutorial](https://www.youtube.com/watch?v=XXXXX)

**Steps:**
1. Choose a YouTube video
2. Set duration to 15-30 seconds
3. Generate 5 clips
4. Select best 2-3 clips
5. Export and upload to TikTok

### Tutorial 2: Create YouTube Shorts

**Video:** [Watch Tutorial](https://www.youtube.com/watch?v=XXXXX)

**Steps:**
1. Select a longer video
2. Set duration to 30-60 seconds
3. Generate 3-4 clips
4. Select best clips
5. Export and upload to YouTube Shorts

### Tutorial 3: Create Instagram Reels

**Video:** [Watch Tutorial](https://www.youtube.com/watch?v=XXXXX)

**Steps:**
1. Choose engaging content
2. Set duration to 30-90 seconds
3. Generate 2-3 clips
4. Export clips
5. Add music in Instagram
6. Upload as Reel

---

## 🆘 Getting Help

### Self-Service
- **Documentation:** Read guides in `docs/` folder
- **FAQ:** Check [FAQ.md](FAQ.md)
- **Troubleshooting:** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### Community
- **GitHub Discussions:** Ask questions
- **GitHub Issues:** Report bugs
- **Discord:** Join our server (coming soon)

### Support
- **Email:** support@example.com
- **Response Time:** 24-48 hours

---

## 📝 Version History

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

---

## 🎉 You're Ready!

Now you know how to use AI Clipper to create viral short-form content.

**Remember:**
- ✅ Add your Gemini API key during setup
- ✅ Choose high-quality videos
- ✅ Experiment with settings
- ✅ Review viral scores
- ✅ Export and upload!

**Happy Clipping! 🚀**

---

**Made with ❤️ by the AI Clipper Team**
**Create Viral Content with AI! 🎬**
