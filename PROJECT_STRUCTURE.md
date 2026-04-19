# AI Clipper - Project Structure

```
ai-clipper/
├── backend/                          # Python backend
│   ├── main.py                       # FastAPI server + WebSocket
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py                 # REST endpoints
│   │   └── websocket.py              # WebSocket handlers
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                 # Configuration management
│   │   └── exceptions.py             # Custom exceptions
│   ├── services/
│   │   ├── __init__.py
│   │   ├── downloader.py             # YouTube video download
│   │   ├── transcriber.py            # Whisper transcription
│   │   ├── analyzer.py               # Gemini AI analysis
│   │   ├── scorer.py                 # Viral moment scoring
│   │   ├── detector.py               # Face/mouth detection
│   │   ├── editor.py                 # Video editing & cutting
│   │   └── cache.py                  # Local caching
│   ├── models/
│   │   ├── __init__.py
│   │   ├── video.py                  # Video data model
│   │   ├── clip.py                   # Clip data model
│   │   └── analysis.py               # Analysis result model
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── video_utils.py            # FFmpeg utilities
│   │   ├── audio_utils.py            # Audio processing
│   │   └── file_utils.py             # File management
│   └── requirements.txt              # Python dependencies
│
├── frontend/                         # Tauri + React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── Layout/
│   │   │   │   ├── MainLayout.tsx
│   │   │   │   ├── LeftPanel.tsx
│   │   │   │   ├── CenterPanel.tsx
│   │   │   │   └── RightPanel.tsx
│   │   │   ├── Input/
│   │   │   │   ├── URLInput.tsx
│   │   │   │   ├── SettingsPanel.tsx
│   │   │   │   └── GenerateButton.tsx
│   │   │   ├── Video/
│   │   │   │   ├── VideoPlayer.tsx
│   │   │   │   ├── ProgressBar.tsx
│   │   │   │   └── Timeline.tsx
│   │   │   ├── Clips/
│   │   │   │   ├── ClipList.tsx
│   │   │   │   ├── ClipCard.tsx
│   │   │   │   └── ClipPreview.tsx
│   │   │   ├── Export/
│   │   │   │   ├── ExportPanel.tsx
│   │   │   │   └── BatchExport.tsx
│   │   │   └── UI/
│   │   │       ├── Loading.tsx
│   │   │       ├── ErrorToast.tsx
│   │   │       └── ProgressOverlay.tsx
│   │   ├── hooks/
│   │   │   ├── useWebSocket.ts       # WebSocket connection
│   │   │   ├── useVideoProcessing.ts # Video processing logic
│   │   │   └── useClips.ts           # Clip management
│   │   ├── services/
│   │   │   ├── api.ts                # REST API client
│   │   │   └── websocket.ts          # WebSocket client
│   │   ├── types/
│   │   │   ├── video.ts
│   │   │   ├── clip.ts
│   │   │   └── api.ts
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── styles/
│   │       └── globals.css
│   ├── src-tauri/
│   │   ├── src/
│   │   │   ├── main.rs
│   │   │   └── lib.rs
│   │   ├── Cargo.toml
│   │   └── tauri.conf.json
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
├── data/
│   ├── downloads/                    # Downloaded videos
│   ├── processed/                    # Processed clips
│   ├── cache/                        # Cached data
│   └── models/                       # AI models (cached)
│
├── docs/
│   ├── API.md                        # API documentation
│   ├── ARCHITECTURE.md               # System architecture
│   └── USER_GUIDE.md                 # User guide
│
├── .env.example                      # Environment variables template
├── .gitignore
├── README.md
└── docker-compose.yml                # Optional: for development
```

## Folder Purposes

### backend/
- **api/**: REST endpoints and WebSocket handlers
- **core/**: Configuration and exception handling
- **services/**: Business logic (download, transcribe, analyze, edit)
- **models/**: Data models and schemas
- **utils/**: Helper utilities

### frontend/
- **components/**: React components organized by feature
- **hooks/**: Custom React hooks for state management
- **services/**: API and WebSocket clients
- **types/**: TypeScript type definitions
- **styles/**: Global styles and themes

### data/
- **downloads/**: Temporary storage for downloaded videos
- **processed/**: Final output clips
- **cache/**: Cached transcriptions, analyses
- **models/**: Downloaded AI models

### docs/
- **API.md**: API endpoints documentation
- **ARCHITECTURE.md**: Detailed architecture decisions
- **USER_GUIDE.md**: End-user documentation
