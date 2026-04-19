# AI Clipper - System Architecture

## Overview

AI Clipper is a modern desktop application that combines:
- **Tauri** for lightweight, native Windows desktop UI
- **Python FastAPI** for backend processing
- **AI/ML** services for intelligent video analysis
- **FFmpeg** for video manipulation

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Desktop Application                      │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │   Left      │  │   Center    │  │   Right     │              │
│  │   Panel     │  │   Panel     │  │   Panel     │              │
│  │             │  │             │  │             │              │
│  │ • URL Input │  │ • Video     │  │ • Clip List │              │
│  │ • Settings  │  │   Preview   │  │ • Thumbnails│              │
│  │ • Generate  │  │ • Timeline  │  │ • Preview   │              │
│  │ • Progress  │  │ • Controls  │  │ • Export    │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
└─────────────────────────────────────────────────────────────┘
                              ↓
                    WebSocket (Real-time)
                    + REST API (Commands)
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      Python Backend                          │
│                                                                  │
│  ┌──────────────────────────────────────────────────────┐    │
│  │                   FastAPI Server                      │    │
│  │  • REST Endpoints (POST /api/generate, etc.)         │    │
│  │  • WebSocket Handler (ws://localhost:8000/ws)        │    │
│  └──────────────────────────────────────────────────────┘    │
│                              ↓                                 │
│  ┌──────────────────────────────────────────────────────┐    │
│  │                  Service Layer                         │    │
│  │                                                        │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐            │    │
│  │  │Download  │  │Transcribe│  │ Analyze  │            │    │
│  │  │Service   │  │ Service  │  │ Service  │            │    │
│  │  └──────────┘  └──────────┘  └──────────┘            │    │
│  │        ↓             ↓             ↓                  │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐            │    │
│  │  │  Score   │  │ Detect   │  │  Edit    │            │    │
│  │  │Service   │  │ Service  │  │ Service  │            │    │
│  │  └──────────┘  └──────────┘  └──────────┘            │    │
│  └──────────────────────────────────────────────────────┘    │
│                              ↓                                 │
│  ┌──────────────────────────────────────────────────────┐    │
│  │                  External Services                     │    │
│  │                                                        │    │
│  │  • yt-dlp (YouTube download)                          │    │
│  │  • Whisper (Transcription)                            │    │
│  │  • Gemini API (Content analysis)                      │    │
│  │  • MediaPipe (Face/mouth detection)                   │    │
│  │  • FFmpeg (Video processing)                          │    │
│  └──────────────────────────────────────────────────────┘    │
│                              ↓                                 │
│  ┌──────────────────────────────────────────────────────┐    │
│  │                  Data Storage                          │    │
│  │                                                        │    │
│  │  • downloads/ (Raw videos)                            │    │
│  │  • processed/ (Generated clips)                       │    │
│  │  • cache/ (Transcriptions, analyses)                  │    │
│  └──────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. User Initiates Generation
```
User Input (URL + Settings)
    ↓
Frontend validates input
    ↓
POST /api/generate (with parameters)
    ↓
Backend creates processing job
    ↓
WebSocket connection established
    ↓
Real-time progress updates sent to frontend
```

### 2. Video Processing Pipeline
```
1. Download (yt-dlp)
   ↓ Video file (mp4)
2. Extract Audio
   ↓ Audio file (wav/mp3)
3. Transcribe (Whisper)
   ↓ Text + Timestamps
4. Analyze (Gemini)
   ↓ Emotional spikes, keywords
5. Score Viral Moments
   ↓ Ranked timestamps
6. Detect Speakers (MediaPipe)
   ↓ Speaker tracking data
7. Cut & Format (FFmpeg)
   ↓ Vertical clips (9:16)
8. Add Subtitles & Effects
   ↓ Final clips ready
```

### 3. WebSocket Communication
```typescript
// Frontend sends
{
  "type": "generate",
  "url": "https://youtube.com/...",
  "settings": {
    "clipDuration": 30,
    "numClips": 5,
    "subtitleStyle": "modern"
  }
}

// Backend sends (stream)
{
  "type": "progress",
  "stage": "downloading",
  "progress": 45,
  "message": "Downloading video... 45%"
}

{
  "type": "clip_generated",
  "clip": {
    "id": "clip_1",
    "startTime": 120,
    "endTime": 150,
    "score": 8.5,
    "thumbnail": "data:image/jpeg,..."
  }
}

{
  "type": "complete",
  "clips": [...]
}
```

## Key Design Decisions

### 1. Tauri vs Electron
| Factor | Tauri | Electron |
|--------|-------|----------|
| Bundle Size | ~5 MB | ~100+ MB |
| Memory | ~50-100 MB | ~200-500 MB |
| Performance | Native | Chromium |
| Security | Rust-based | JavaScript |
| Dev Experience | Modern | Mature |

**Decision**: Tauri for lightweight, native performance.

### 2. Python Backend
- **Why?** Best AI/ML ecosystem
- **FastAPI**: Async, fast, modern
- **WebSocket**: Real-time progress updates
- **Separate process**: Isolates heavy processing

### 3. Service Layer Architecture
- **Modular**: Each service is independent
- **Testable**: Easy to unit test
- **Scalable**: Can add more services
- **Cacheable**: Results can be cached

### 4. Viral Moment Scoring Algorithm
```python
Score = (
  0.3 * emotional_intensity +
  0.25 * keyword_relevance +
  0.2 * speaker_engagement +
  0.15 * pacing_variation +
  0.1 * scene_changes
)
```

### 5. Speaker Detection Strategy
```python
# MediaPipe Face Mesh
- Detect faces in each frame
- Track mouth landmarks (lips)
- Calculate mouth movement intensity
- Identify active speaker
- Crop/zoom to speaker
```

## Performance Optimization

### 1. Caching Strategy
```python
cache_key = f"{video_id}_{resolution}_transcription"
if cache.exists(cache_key):
    return cache.get(cache_key)
# Process and cache result
```

### 2. Parallel Processing
```python
# Process multiple clips in parallel
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(process_clip, clip) for clip in clips]
```

### 3. Video Streaming
```python
# Stream video instead of loading full file
ffmpeg.input(url).output(
    '-',
    format='mp4',
    vcodec='libx264',
    acodec='aac'
).run(capture_stdout=True)
```

### 4. Lazy Loading
```python
# Load AI models on demand
@lru_cache(maxsize=1)
def get_whisper_model():
    return whisper.load_model("base")
```

## Error Handling

### 1. Frontend Validation
```typescript
const validateURL = (url: string): boolean => {
  const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+$/
  return youtubeRegex.test(url)
}
```

### 2. Backend Validation
```python
def validate_youtube_url(url: str) -> bool:
    ydl_opts = {'quiet': True}
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return info is not None
        except:
            return False
```

### 3. Graceful Degradation
```python
try:
    # Try AI enhancement
    clips = enhance_with_ai(clips)
except Exception as e:
    logger.warning(f"AI enhancement failed: {e}")
    # Fall back to basic processing
    clips = basic_processing(clips)
```

## Security Considerations

1. **API Keys**: Store in environment variables
2. **Input Validation**: Sanitize all inputs
3. **File Paths**: Use safe path joining
4. **Rate Limiting**: Implement API rate limits
5. **CORS**: Configure allowed origins

## Deployment Strategy

### Development
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run tauri dev
```

### Production Build
```bash
# Backend: Package as standalone executable
pyinstaller --onefile backend/main.py

# Frontend: Build Tauri app
cd frontend
npm run tauri build
```

## Monitoring & Logging

```python
# Structured logging
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai-clipper.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

## Future Enhancements

1. **Batch Processing**: Process multiple videos
2. **Custom Templates**: User-defined clip styles
3. **Social Media Integration**: Direct upload
4. **Analytics**: Track clip performance
5. **AI Voice Enhancement**: Improve audio quality
6. **Auto B-Roll**: Add relevant B-roll footage
