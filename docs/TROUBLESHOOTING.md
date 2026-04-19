# 🔧 Troubleshooting Guide

## 📋 Common Issues & Solutions

This guide covers the most common issues users encounter and how to resolve them.

---

## 🚨 Critical Issues

### Issue: Application Won't Start

**Symptoms:**
- Double-clicking the application does nothing
- Error message appears and closes immediately

**Solutions:**

1. **Check System Requirements**
   ```
   Required: Windows 10 or later (64-bit)
   RAM: 8 GB minimum
   Storage: 5 GB free space
   ```

2. **Run as Administrator**
   - Right-click "AI Clipper"
   - Select "Run as administrator"

3. **Check Windows Defender**
   - Open Windows Security
   - Go to "Virus & threat protection"
   - Click "Manage settings"
   - Add "AI Clipper" to exclusions

4. **Reinstall Application**
   - Uninstall from Control Panel
   - Download latest installer
   - Reinstall

5. **Check Event Viewer**
   - Press `Win + X`, select "Event Viewer"
   - Go to "Windows Logs" → "Application"
   - Look for errors related to AI Clipper

---

### Issue: "Windows Protected Your PC"

**Symptoms:**
- Warning when opening installer or application
- "Windows protected your PC" message

**Solutions:**

1. **Click "More Info" → "Run anyway"**
   - This is normal for unsigned applications
   - Safe to proceed for AI Clipper

2. **Add to Windows Defender Exclusions**
   ```
   Settings → Update & Security → Windows Security
   → Virus & threat protection → Manage settings
   → Exclusions → Add or remove exclusions
   → Add an exclusion → Folder
   → Select AI Clipper installation folder
   ```

3. **Disable SmartScreen (Temporary)**
   ```
   Windows Security → App & browser control
   → Check apps and files → Off
   (Enable after installation)
   ```

**Note:** This warning appears because AI Clipper is not digitally signed. For public distribution, consider getting a code signing certificate.

---

## 📥 Download Issues

### Issue: "Invalid URL" Error

**Symptoms:**
- Error message when pasting YouTube URL
- Application doesn't recognize the URL

**Solutions:**

1. **Use Valid YouTube URL Format**
   ```
   ✅ Valid: https://www.youtube.com/watch?v=xxxxx
   ✅ Valid: https://youtu.be/xxxxx
   ❌ Invalid: www.youtube.com/watch?v=xxxxx
   ❌ Invalid: https://youtube.com/xxxxx
   ```

2. **Get URL Directly from YouTube**
   - Open video on YouTube
   - Click "Share"
   - Copy the URL
   - Paste into AI Clipper

3. **Check for Typos**
   - Ensure `https://` is present
   - Verify `youtube.com` or `youtu.be` domain
   - Check for extra spaces or characters

4. **Try a Different Video**
   - Some videos may be restricted
   - Private videos won't work
   - Age-restricted videos may fail

---

### Issue: Download Stuck or Very Slow

**Symptoms:**
- Download progress stuck at same percentage
- Download taking too long

**Solutions:**

1. **Check Internet Connection**
   - Ensure stable internet connection
   - Try loading YouTube in browser
   - Check if YouTube is accessible

2. **Restart Download**
   - Cancel current download
   - Close and reopen application
   - Try downloading again

3. **Clear Cache**
   - Go to Settings → Advanced
   - Click "Clear Cache"
   - Retry download

4. **Check YouTube Status**
   - Verify YouTube is up (https://status.google.com/)
   - Some regions may have YouTube restrictions

5. **Use VPN (If in restricted region)**
   - Some countries block YouTube
   - Try using a VPN to access YouTube

---

## 🔑 API Key Issues

### Issue: "API Key Required" Error

**Symptoms:**
- Error message about missing API key
- Application won't process videos

**Solutions:**

1. **Get a Gemini API Key**
   - Visit: https://makersuite.google.com/app/apikey
   - Sign in with Google account
   - Click "Create API key"
   - Copy the key

2. **Enter API Key in Application**
   - Open AI Clipper
   - Go to Settings → API
   - Paste the API key
   - Click "Save"
   - Restart application

3. **Verify API Key is Valid**
   - Check for extra spaces or characters
   - Ensure key starts with `AIza`
   - Regenerate key if needed

4. **Check API Key Quota**
   - Visit: https://console.cloud.google.com/
   - Check API usage limits
   - Free tier: 1,500 requests/day
   - Upgrade if quota exceeded

---

### Issue: "API Quota Exceeded" Error

**Symptoms:**
- Error about API limits
- Processing stops mid-way

**Solutions:**

1. **Check Your Quota**
   - Visit: https://console.cloud.google.com/
   - Go to APIs & Services → Quotas
   - Check Gemini API usage

2. **Wait for Reset**
   - Free quota resets daily
   - Check reset time in Google Console

3. **Reduce Usage**
   - Process fewer videos
   - Generate fewer clips per video
   - Increase clip duration to reduce API calls

4. **Upgrade to Paid Plan**
   - Gemini pricing: ~$0.001 per request
   - Set billing account in Google Console
   - Quota will increase automatically

---

## 🎬 Processing Issues

### Issue: Processing Takes Too Long

**Symptoms:**
- Processing exceeds expected time
- Progress bar stuck

**Expected Times:**
- Short video (5-10 min): 3-5 minutes
- Medium video (10-30 min): 5-10 minutes
- Long video (30-60 min): 10-20 minutes

**Solutions:**

1. **Close Other Applications**
   - Free up CPU and RAM
   - Close browser tabs
   - Close other video editors

2. **Check System Resources**
   - Open Task Manager (Ctrl + Shift + Esc)
   - Check CPU and RAM usage
   - Ensure 50%+ resources available

3. **Optimize Settings**
   - Reduce number of clips (e.g., 3 instead of 10)
   - Increase clip duration (e.g., 60s instead of 30s)
   - Disable unnecessary features

4. **Check Storage**
   - Ensure sufficient disk space (5 GB+)
   - Use SSD for faster I/O
   - Clear temporary files

5. **Restart Application**
   - Cancel current processing
   - Close and reopen AI Clipper
   - Try again with shorter video

---

### Issue: Processing Failed Mid-Way

**Symptoms:**
- Error message during processing
- Progress stops suddenly

**Solutions:**

1. **Check Error Message**
   - Read the error details carefully
   - Note which stage failed
   - Check for specific error codes

2. **Common Failures:**
   - **Download failed:** Check internet connection
   - **Transcription failed:** Check API key, audio quality
   - **Analysis failed:** Check API quota
   - **Export failed:** Check disk space, file permissions

3. **Check Logs**
   - Go to Settings → Advanced → View Logs
   - Look for error messages
   - Copy logs for support

4. **Retry Processing**
   - Cancel and restart processing
   - Try with different settings
   - Ensure sufficient resources

5. **Check Video Quality**
   - Ensure video is accessible
   - Verify audio track exists
   - Try with a different video

---

## 📤 Export Issues

### Issue: Export Failed

**Symptoms:**
- Error when exporting clips
- No output files created

**Solutions:**

1. **Check Disk Space**
   - Ensure 1-2 GB free per clip
   - Choose different output location
   - Clear disk space if needed

2. **Check File Permissions**
   - Ensure write access to output folder
   - Try exporting to Documents folder
   - Run as Administrator

3. **Close Other Applications**
   - Close video players
   - Close other editors
   - Free up resources

4. **Export One Clip at a Time**
   - Try exporting single clip
   - Identify problematic clip
   - Disable problematic clips

5. **Restart Application**
   - Close and reopen AI Clipper
   - Retry export

---

### Issue: Exported Video Quality is Poor

**Symptoms:**
- Blurry or pixelated video
- Low resolution output

**Solutions:**

1. **Check Source Quality**
   - Ensure original video is 720p or higher
   - Avoid low-quality sources
   - Use HD videos for best results

2. **Check Export Settings**
   - Ensure quality is set to 1080p
   - Check if compression is too high
   - Verify format settings

3. **Check Player**
   - Try playing in different player (VLC, Windows Media Player)
   - Upload to YouTube/TikTok to verify
   - Check if quality issue is player-related

4. **Update Application**
   - Ensure using latest version
   - Check for bug fixes
   - Reinstall if needed

---

## 🎨 UI/UX Issues

### Issue: Application Not Responsive

**Symptoms:**
- UI freezes during processing
- Buttons don't respond
- Progress bar stuck

**Solutions:**

1. **Wait for Processing**
   - Processing may take time
   - Check if CPU is being used
   - Wait 1-2 minutes

2. **Check for Crashes**
   - Look for crash reports
   - Check Event Viewer
   - Restart application

3. **Close and Reopen**
   - Wait for current operation to complete
   - Close application
   - Reopen and try again

4. **Reduce Load**
   - Process shorter videos
   - Generate fewer clips
   - Close other applications

---

### Issue: Clips Not Showing in List

**Symptoms:**
- Processing completes but no clips appear
- List is empty or incomplete

**Solutions:**

1. **Wait for Processing to Complete**
   - Ensure progress bar reached 100%
   - Check status message
   - Wait 1-2 minutes after completion

2. **Refresh the List**
   - Close and reopen application
   - Re-load the video
   - Check if clips appear

3. **Check Settings**
   - Ensure clips are enabled
   - Check filters or search
   - Reset view settings

4. **Check Logs**
   - Go to Settings → Advanced → View Logs
   - Look for errors
   - Check if clips were generated

---

## 🔧 Advanced Troubleshooting

### View Application Logs

1. Open AI Clipper
2. Go to Settings → Advanced
3. Click "View Logs"
4. Look for error messages
5. Copy logs for support

### Clear Cache

1. Open AI Clipper
2. Go to Settings → Advanced
3. Click "Clear Cache"
4. Confirm
5. Restart application

### Reset Settings

1. Close AI Clipper
2. Delete settings folder:
   ```
   %APPDATA%\ai-clipper\
   ```
3. Restart application
4. Reconfigure settings

### Reinstall Application

1. Uninstall from Control Panel
2. Delete remaining folders:
   ```
   %APPDATA%\ai-clipper\
   %LOCALAPPDATA%\ai-clipper\
   ```
3. Download latest installer
4. Reinstall
5. Reconfigure settings

---

## 📞 Getting Help

### Still Having Issues?

1. **Check Documentation**
   - [FAQ](FAQ.md) - Common questions
   - [User Guide](USER_GUIDE.md) - Complete manual
   - [API Reference](API_REFERENCE.md) - Technical details

2. **Search GitHub Issues**
   - Check if issue is already reported
   - Look for workarounds
   - Add your experience to existing issue

3. **Create New Issue**
   - Provide detailed description
   - Include error messages
   - Attach logs if possible
   - Specify your system specs

4. **Contact Support**
   - Email: support@example.com
   - Include: OS, app version, error details, logs

---

## 📊 System Information for Support

When requesting help, include:

```
System Information:
- OS: Windows 10/11 (Version: ...)
- RAM: 8/16/32 GB
- Storage: HDD/SSD, X GB free
- AI Clipper Version: 1.0.0

Issue Details:
- What were you doing?
- What happened?
- What did you expect?
- Error message (if any)

Steps to Reproduce:
1. Step 1
2. Step 2
3. Step 3

Logs:
[Attach or paste relevant logs]
```

---

**Made with ❤️ by the AI Clipper Team**
**Don't hesitate to ask for help! 💬**
