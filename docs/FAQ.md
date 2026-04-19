# ❓ Frequently Asked Questions (FAQ)

## 📋 General Questions

### What is AI Clipper?

AI Clipper is a desktop application that automatically generates short-form video clips from YouTube videos. It uses AI to identify the most engaging moments and creates optimized clips for TikTok, YouTube Shorts, and Instagram Reels.

### Is AI Clipper free?

The application is free, but it requires a Gemini API key for AI processing. Gemini offers a free tier that allows for substantial usage. For heavy use, you may need to upgrade to a paid plan.

### What platforms does AI Clipper support?

Currently, AI Clipper is available for Windows 10 and later (64-bit). We're working on macOS and Linux versions for future releases.

### Do I need a powerful computer?

**Minimum requirements:**
- Windows 10 or later
- 8 GB RAM
- 5 GB free storage
- Internet connection

**Recommended:**
- 16 GB RAM
- SSD storage
- Dedicated GPU (optional, for faster processing)

---

## 🎬 Usage Questions

### How long does it take to process a video?

Processing time depends on video length and settings:

- **Short video (5-10 min):** 3-5 minutes
- **Medium video (10-30 min):** 5-10 minutes
- **Long video (30-60 min):** 10-20 minutes

Factors that affect speed:
- Video length
- Number of clips requested
- Computer specifications
- Internet speed

### Can I process videos from sources other than YouTube?

Currently, only YouTube videos are supported. We're working on adding support for other platforms (Vimeo, TikTok, Instagram) in future updates.

### What's the maximum number of clips I can generate?

You can generate up to 10 clips from a single video. Each clip can be 15-60 seconds long.

### Can I customize the clips after generation?

Yes! You can:
- Enable/disable clips for export
- Preview clips before export
- Adjust clip settings before regenerating
- Export individual clips or in batches

### Can I add my own music?

Currently, music addition is not supported. However, you can add music after export using video editing software or platform tools (TikTok, Instagram, etc.).

### What video quality will I get?

All exported clips are:
- Format: MP4 (H.264 codec)
- Resolution: 1080x1920 (9:16 vertical)
- Bitrate: Optimized for social media
- Quality: HD (high definition)

---

## 🔑 API Key Questions

### Do I need an API key?

Yes, you need a Gemini API key for AI content analysis.

### How do I get a Gemini API key?

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API key"
4. Copy the key and paste it into AI Clipper

### Is the Gemini API free?

Gemini offers a free tier that includes:
- 15 requests per minute
- 1,500 requests per day

This is sufficient for personal use. For commercial or heavy use, you may need a paid plan starting at $0.001 per request.

### Is my API key secure?

Yes, your API key is stored locally on your computer and is never shared with third parties. It's only used to communicate with Google's servers for AI processing.

### Can I use a different AI service?

Currently, only Gemini is supported. We're considering adding support for other AI services (OpenAI, Claude) in future updates.

---

## ⚠️ Legal & Copyright

### Is it legal to download YouTube videos?

YouTube's Terms of Service prohibit downloading videos without permission. However, AI Clipper is designed for:
- Personal use
- Educational purposes
- Transformative works (short clips)
- Fair use applications

**Important:**
- Always respect copyright laws
- Use responsibly and ethically
- Get permission when possible
- Don't download restricted content

### Can I use generated clips commercially?

Yes, if:
- The original video is your own content
- You have permission from the content owner
- The use qualifies as fair use

**Disclaimer:** You are responsible for ensuring your use complies with copyright laws.

### Will AI Clipper add watermarks?

No, AI Clipper does not add watermarks to generated clips. You own the output.

---

## 🐛 Troubleshooting

### "Invalid URL" error

**Solutions:**
1. Make sure it's a valid YouTube URL
2. Try using the share link from YouTube
3. Check for typos
4. Try a different video

### "Download failed" error

**Solutions:**
1. Check internet connection
2. Try a different video
3. Some videos may be age-restricted or private
4. Check if YouTube is blocked in your region

### "API key required" error

**Solutions:**
1. Get a free API key: https://makerspace.google.com/app/apikey
2. Paste the key in application settings
3. Click "Save"
4. Restart the application

### "Export failed" error

**Solutions:**
1. Check disk space
2. Choose a different output location
3. Close other applications
4. Try exporting one clip at a time
5. Check file permissions

### "Processing too slow"

**Normal processing times:**
- Short video: 3-5 minutes
- Medium video: 5-10 minutes
- Long video: 10-20 minutes

**To speed up:**
1. Close other applications
2. Use SSD storage
3. Increase RAM (upgrade to 16 GB)
4. Reduce number of clips requested
5. Shorten clip duration

### Application crashes

**Solutions:**
1. Restart the application
2. Check for updates
3. Ensure sufficient RAM available
4. Check disk space
5. Reinstall the application

---

## 🔧 Technical Questions

### What programming languages is AI Clipper built with?

- **Frontend:** React, TypeScript, Tauri
- **Backend:** Python, FastAPI
- **AI/ML:** Whisper, Gemini, MediaPipe
- **Video Processing:** FFmpeg, yt-dlp, OpenCV

### Can I run AI Clipper on Linux or Mac?

Currently, only Windows is supported. We're working on macOS and Linux versions for future releases.

### Is the application open source?

Yes! AI Clipper is open source. You can view the source code and contribute on GitHub.

### Can I build AI Clipper from source?

Yes, see [BUILD_GUIDE.md](BUILD_GUIDE.md) for detailed build instructions.

### Does AI Clipper work offline?

No, AI Clipper requires an internet connection for:
- Downloading YouTube videos
- AI processing (transcription and analysis)
- Content generation

However, some features (preview, export) can work offline after initial processing.

---

## 📊 Performance & Limits

### What's the maximum video length supported?

There's no hard limit, but for best results:
- **Optimal:** 5-30 minutes
- **Maximum:** Up to 2 hours
- **Not recommended:** Very long videos (>2 hours)

### How much storage space do I need?

Per video processing:
- Temporary files: ~1-2 GB
- Exported clips: ~50-200 MB per clip
- Recommendation: 5 GB free minimum

### Can I process multiple videos at once?

Currently, only one video at a time is supported. We're working on batch processing for future releases.

### How many clips can I generate?

- **Minimum:** 1 clip
- **Maximum:** 10 clips
- **Recommended:** 3-5 clips for best results

---

## 🔄 Updates & Support

### How do I update AI Clipper?

Updates are automatic when available. You can also:
1. Check GitHub for new releases
2. Download the latest installer
3. Reinstall (your settings will be preserved)

### Where can I get support?

- **Documentation:** Check the [docs/](.) folder
- **GitHub Issues:** Report bugs and request features
- **Community:** Join discussions (coming soon)
- **Email:** support@example.com

### How can I request new features?

We welcome feature requests! Please:
1. Check if it's already requested (GitHub Issues)
2. Create a new issue with detailed description
3. Explain the use case and benefits
4. We'll review and prioritize

---

## 📈 Future Roadmap

### What's coming next?

**v1.1 (Planned):**
- TikTok direct upload
- Instagram direct upload
- YouTube Shorts direct upload
- Custom subtitle styles
- Background music library

**v2.0 (Future):**
- Batch processing
- AI voiceover generation
- Advanced effects
- Cloud rendering
- Team collaboration

### How can I stay updated?

- Star the GitHub repository
- Watch for releases
- Join our newsletter (coming soon)
- Follow on social media (coming soon)

---

## 💡 Pro Tips

### 1. Best Settings for TikTok
- Duration: 15-30 seconds
- Number of clips: 3-5
- Subtitles: Essential
- Jump cuts: Recommended

### 2. Best Settings for YouTube Shorts
- Duration: 30-60 seconds
- Number of clips: 2-4
- Quality: 1080p
- Hook: First 3 seconds crucial

### 3. Best Settings for Instagram Reels
- Duration: 30-90 seconds
- Number of clips: 2-3
- Music: Add in Instagram
- Trending: Use trending audio

### 4. Tips for Higher Viral Scores
- Choose videos with emotional content
- Look for controversial or surprising moments
- Select clips with clear hooks
- Ensure good audio quality
- Optimize for your target audience

---

## 📞 Still Have Questions?

If your question isn't answered here:

1. **Check Documentation:** Review the [docs/](.) folder
2. **Search Issues:** Look for similar issues on GitHub
3. **Ask Community:** Join discussions (coming soon)
4. **Contact Us:** support@example.com

---

**Made with ❤️ by the AI Clipper Team**
**Happy Clipping! 🚀**
