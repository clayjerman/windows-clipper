# 🔑 API Key Setup Guide

## Overview

AI Clipper requires API keys for AI-powered features. Users are prompted to enter their API keys when they first launch the application.

---

## 📋 Required API Keys

### 1. Gemini API Key (Required)

**Purpose:** Content analysis, viral moment detection, and AI insights

**How to Get:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API key"
4. Copy the API key (starts with `AIza`)
5. Paste it in the application setup screen

**Free Tier:**
- 1,500 requests per day
- 15 requests per minute
- Sufficient for personal use

**Paid Tier:**
- Starts at $0.001 per request
- Higher limits available
- Suitable for commercial use

---

### 2. OpenAI API Key (Optional)

**Purpose:** Additional AI features (optional, can be added later in Settings)

**How to Get:**
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Go to "API Keys" section
4. Click "Create new secret key"
5. Copy the API key (starts with `sk-`)
6. Add it in Settings (optional)

**Note:** This key is NOT required for basic functionality. The app works with just the Gemini API key.

---

## 🚀 First-Time Setup

### When You Launch the App

1. **Onboarding Screen** appears automatically
2. **Required Field:** Gemini API Key
3. **Optional Field:** OpenAI API Key
4. Click "Save & Continue"

### What Happens

- API keys are stored securely in your browser's localStorage
- Keys are NEVER sent to any third-party servers
- Keys are ONLY used to communicate with Google/OpenAI APIs

### Skipping Setup

You can skip the setup, but:
- ❌ You won't be able to use AI features
- ❌ Video processing will fail
- ❌ You'll need to add the key later in Settings

**Recommendation:** Add your Gemini API key during setup for the best experience.

---

## 🔧 Managing API Keys

### Adding/Changing Keys

1. Open AI Clipper
2. Click **Settings** in the top-right
3. Find **API Keys** section
4. Enter your new keys
5. Click **Save**

### Clearing Keys

1. Open Settings
2. Click **Clear Keys** button
3. Confirm the action
4. Keys will be removed from storage

### Testing Keys

In Settings, click **Test Key** to verify:
- Key format is correct
- Key can communicate with API
- Key has sufficient quota

---

## 🔒 Security

### How Keys Are Stored

- **Location:** Browser's localStorage
- **Encryption:** Not encrypted (local storage only)
- **Access:** Only by AI Clipper application
- **Sharing:** NEVER shared with third parties

### Best Practices

✅ **DO:**
- Use free API keys for personal use
- Get keys from official sources (Google, OpenAI)
- Keep your keys private
- Update keys if compromised

❌ **DON'T:**
- Share your API keys with others
- Post keys in public forums or GitHub
- Use keys from untrusted sources
- Commit keys to version control

### What If Keys Are Compromised?

1. Go to Google AI Studio / OpenAI Platform
2. Delete the compromised key
3. Create a new key
4. Update the key in AI Clipper Settings

---

## 💡 Troubleshooting

### Issue: "Invalid API Key"

**Solutions:**
- Check that the key starts with `AIza` (Gemini) or `sk-` (OpenAI)
- Ensure no extra spaces or characters
- Verify the key is copied completely
- Try regenerating a new key

### Issue: "API Quota Exceeded"

**Solutions:**
- Check your usage in Google Console
- Wait for daily quota reset (free tier)
- Upgrade to paid plan if needed
- Reduce number of clips per video

### Issue: "API Key Not Found"

**Solutions:**
- Open Settings
- Re-enter your API key
- Click Save
- Restart the application

### Issue: Features Not Working

**Solutions:**
- Ensure Gemini API key is entered
- Test the key in Settings
- Check internet connection
- Verify API key has sufficient quota

---

## 📊 Cost Estimation

### Gemini API (Free Tier)

- **Cost:** Free
- **Limit:** 1,500 requests/day
- **Sufficient for:** ~10-20 videos/day (depends on length)

### Gemini API (Paid Tier)

- **Cost:** ~$0.001 per request
- **Example:** Processing 100 videos = ~$0.10
- **Monthly estimate:** $3-10 for heavy users

### OpenAI API (Optional)

- **Cost:** Varies by model
- **GPT-4:** ~$0.03 per 1K tokens
- **GPT-3.5:** ~$0.002 per 1K tokens
- **Usage:** Minimal (optional features only)

---

## 🔗 Official Resources

### Google Gemini
- **Get API Key:** https://makersuite.google.com/app/apikey
- **Documentation:** https://ai.google.dev/docs
- **Pricing:** https://ai.google.dev/pricing
- **Console:** https://console.cloud.google.com/

### OpenAI
- **Get API Key:** https://platform.openai.com/api-keys
- **Documentation:** https://platform.openai.com/docs
- **Pricing:** https://openai.com/pricing

---

## 📝 Summary

### Required
- ✅ **Gemini API Key** - For all AI features

### Optional
- ⭕ **OpenAI API Key** - For additional features

### Setup Time
- **First time:** 2-3 minutes
- **Updates:** 1 minute in Settings

### Cost
- **Free tier:** Sufficient for most users
- **Paid tier:** $0.001 per request

### Security
- 🔒 Stored locally
- 🔒 Never shared
- 🔒 Easy to update/clear

---

## ❓ FAQ

### Q: Do I need both API keys?
**A:** No, only Gemini is required. OpenAI is optional.

### Q: Can I use the app without API keys?
**A:** No, AI features require API keys. The app will prompt you to add them.

### Q: Are my API keys safe?
**A:** Yes, they're stored locally on your device and never shared.

### Q: What happens if I exceed my free quota?
**A:** You'll need to wait for the daily reset or upgrade to a paid plan.

### Q: Can I use the same key on multiple computers?
**A:** Yes, you can use the same API key on multiple devices.

### Q: How do I know if my key is working?
**A:** Click "Test Key" in Settings to verify.

---

**Made with ❤️ by the AI Clipper Team**
**Secure API Key Management! 🔒**
