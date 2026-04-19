"""
AI Clipper - Main FastAPI Server
"""
import os
import logging
import asyncio
from typing import List, Optional
from datetime import datetime
import uuid

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel

from .core.config import settings
from .core.exceptions import AIClipperError
from .models.video import (
    Video,
    VideoMetadata,
    ClipSettings,
    ProcessingProgress,
    Transcription
)
from .models.clip import Clip, ClipExport, ExportResult
from .models.analysis import ContentAnalysis, ViralScoreResult

from .services.downloader import VideoDownloader
from .services.transcriber import Transcriber
from .services.analyzer import ContentAnalyzer
from .services.scorer import ViralScorer
from .services.detector import MouthTracker
from .services.editor import VideoEditor
from .services.cache import CacheService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="AI Clipper API",
    description="API for generating viral short-form clips from YouTube videos",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global services (analyzer is created per-request with the user's API key)
downloader = VideoDownloader()
transcriber = Transcriber()
scorer = ViralScorer()
mouth_tracker = MouthTracker()
editor = VideoEditor()
cache = CacheService()

# Active WebSocket connections
active_connections: List[WebSocket] = []

# Processing jobs (in production, use Redis or similar)
processing_jobs = {}


# Pydantic models for API
class GenerateRequest(BaseModel):
    url: str
    settings: ClipSettings = ClipSettings()
    gemini_api_key: str = ""


class GenerateResponse(BaseModel):
    job_id: str
    status: str
    message: str


class VideoInfoRequest(BaseModel):
    url: str


class VideoInfoResponse(BaseModel):
    metadata: VideoMetadata
    valid: bool


# API Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "AI Clipper API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/video/info", response_model=VideoInfoResponse)
async def get_video_info(request: VideoInfoRequest):
    """Get video metadata without downloading"""
    try:
        metadata = downloader.get_video_info(request.url)
        return VideoInfoResponse(metadata=metadata, valid=True)
    except Exception as e:
        logger.error(f"Failed to get video info: {e}")
        return VideoInfoResponse(
            metadata=VideoMetadata(
                video_id="",
                title="",
                author="",
                duration=0
            ),
            valid=False
        )


@app.post("/api/generate", response_model=GenerateResponse)
async def generate_clips(request: GenerateRequest, background_tasks: BackgroundTasks):
    """
    Generate clips from YouTube video

    This initiates an async background job that:
    1. Downloads the video
    2. Transcribes audio
    3. Analyzes content with AI
    4. Scores viral moments
    5. Detects speakers
    6. Generates clips
    """
    try:
        # Validate URL
        if not downloader.validate_url(request.url):
            raise HTTPException(status_code=400, detail="Invalid YouTube URL")

        # Create job ID
        job_id = str(uuid.uuid4())

        # Initialize job status
        processing_jobs[job_id] = {
            "status": "pending",
            "url": request.url,
            "settings": request.settings.dict(),
            "created_at": datetime.utcnow(),
            "progress": 0,
            "clips": []
        }

        # Start background processing
        background_tasks.add_task(
            process_video_job,
            job_id,
            request.url,
            request.settings,
            request.gemini_api_key,
        )

        return GenerateResponse(
            job_id=job_id,
            status="started",
            message="Video processing started"
        )

    except Exception as e:
        logger.error(f"Failed to start generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/job/{job_id}")
async def get_job_status(job_id: str):
    """Get status of a processing job"""
    if job_id not in processing_jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    return processing_jobs[job_id]


@app.get("/api/job/{job_id}/clips")
async def get_job_clips(job_id: str):
    """Get clips generated by a job"""
    if job_id not in processing_jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "clips": processing_jobs[job_id].get("clips", [])
    }


@app.post("/api/export")
async def export_clips(request: ClipExport, background_tasks: BackgroundTasks):
    """Export selected clips"""
    job_id = str(uuid.uuid4())

    background_tasks.add_task(export_clips_job, job_id, request)

    return {
        "job_id": job_id,
        "status": "started",
        "message": "Export started"
    }


@app.get("/api/clips/{clip_id}/video")
async def get_clip_video(clip_id: str):
    """Stream a generated clip video file"""
    for job_data in processing_jobs.values():
        clips = job_data.get("clips", [])
        clip = next((c for c in clips if c["id"] == clip_id), None)
        if clip and clip.get("video_path") and os.path.exists(clip["video_path"]):
            return FileResponse(
                clip["video_path"],
                media_type="video/mp4",
                headers={"Accept-Ranges": "bytes"},
            )
    raise HTTPException(status_code=404, detail="Clip not found")


@app.get("/api/clips/{clip_id}/thumbnail")
async def get_clip_thumbnail(clip_id: str):
    """Return thumbnail image for a clip"""
    for job_data in processing_jobs.values():
        clips = job_data.get("clips", [])
        clip = next((c for c in clips if c["id"] == clip_id), None)
        if clip and clip.get("thumbnail_path") and os.path.exists(clip["thumbnail_path"]):
            return FileResponse(clip["thumbnail_path"], media_type="image/jpeg")
    raise HTTPException(status_code=404, detail="Thumbnail not found")


@app.get("/api/export/directory")
async def get_export_directory():
    """Return the directory where processed clips are saved"""
    return {"path": settings.PROCESSED_DIR}


@app.get("/api/cache/stats")
async def get_cache_stats():
    """Get cache statistics"""
    return cache.get_cache_stats()


@app.delete("/api/cache")
async def clear_cache():
    """Clear all cache"""
    count = cache.clear_all()
    return {
        "message": f"Cleared {count} cache entries",
        "count": count
    }


# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time progress updates"""
    await websocket.accept()
    active_connections.append(websocket)

    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
            logger.debug(f"WebSocket received: {data}")

    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logger.info("WebSocket disconnected")


# Helper functions
async def broadcast_progress(job_id: str, progress: ProcessingProgress):
    """Send progress update to all connected clients"""
    message = {
        "type": "progress",
        "job_id": job_id,
        "data": progress.dict()
    }

    for connection in active_connections:
        try:
            await connection.send_json(message)
        except Exception as e:
            logger.warning(f"Failed to send progress: {e}")


async def broadcast_clip_generated(job_id: str, clip: Clip):
    """Send new clip notification to all clients"""
    message = {
        "type": "clip_generated",
        "job_id": job_id,
        "data": clip.dict()
    }

    for connection in active_connections:
        try:
            await connection.send_json(message)
        except Exception as e:
            logger.warning(f"Failed to send clip: {e}")


async def broadcast_complete(job_id: str, clips: List[Clip]):
    """Send completion notification to all clients"""
    message = {
        "type": "complete",
        "job_id": job_id,
        "data": {
            "clips": [clip.dict() for clip in clips]
        }
    }

    for connection in active_connections:
        try:
            await connection.send_json(message)
        except Exception as e:
            logger.warning(f"Failed to send complete: {e}")


async def process_video_job(
    job_id: str,
    url: str,
    clip_settings: ClipSettings,
    gemini_api_key: str = "",
):
    """
    Main video-processing pipeline.

    Improvements vs. original:
    - Async download with live progress broadcast
    - In-process metadata cache (lru_cache in downloader)
    - Parallel clip rendering via asyncio + ThreadPoolExecutor
    - All per-clip FFmpeg work runs in a single pass (editor.process_clip)
    """
    loop = asyncio.get_event_loop()

    async def _progress(stage: str, pct: int, msg: str, **kw):
        await broadcast_progress(
            job_id,
            ProcessingProgress(stage=stage, progress=pct, message=msg, **kw),
        )

    async def _error(msg: str):
        processing_jobs[job_id]["status"] = "failed"
        processing_jobs[job_id]["error"] = msg
        for conn in list(active_connections):
            try:
                await conn.send_json({"type": "error", "job_id": job_id, "data": {"error": msg}})
            except Exception:
                pass

    try:
        logger.info(f"Job {job_id} started: {url}")
        processing_jobs[job_id]["status"] = "downloading"

        # ── Step 1: Download ──────────────────────────────────────────────────
        await _progress("downloading", 0, "Fetching video info…")
        metadata = downloader.get_video_info(url)

        last_pct: list[int] = [0]

        def _dl_progress(message: str, pct: int):
            if pct != last_pct[0]:
                last_pct[0] = pct
                # schedule coroutine from thread
                asyncio.run_coroutine_threadsafe(
                    _progress("downloading", pct, message),
                    loop,
                )

        quality = "720p" if clip_settings.output_resolution <= 720 else "1080p"
        video_path = await downloader.download_async(url, quality=quality, progress_callback=_dl_progress)
        processing_jobs[job_id]["video_path"] = video_path
        await _progress("downloading", 100, "Download complete")

        # ── Step 2: Transcribe ────────────────────────────────────────────────
        processing_jobs[job_id]["status"] = "transcribing"
        await _progress("transcribing", 0, "Starting transcription…")

        cached_transcription = cache.get_video_transcription(metadata.video_id)
        if cached_transcription:
            transcription = Transcription(**cached_transcription)
            logger.info("Using cached transcription")
        else:
            transcription = await loop.run_in_executor(
                None, transcriber.transcribe_video, video_path
            )
            cache.set_video_transcription(metadata.video_id, transcription.dict())

        await _progress("transcribing", 100, "Transcription complete")

        # ── Step 3: Analyse ───────────────────────────────────────────────────
        processing_jobs[job_id]["status"] = "analyzing"
        await _progress("analyzing", 0, "Analysing content with AI…")

        api_key = gemini_api_key or settings.GEMINI_API_KEY
        if not api_key:
            await _error("Gemini API key not configured. Please add it in Settings.")
            return

        analyzer = ContentAnalyzer(api_key=api_key)

        cached_analysis = cache.get_video_analysis(metadata.video_id)
        if cached_analysis:
            analysis = ContentAnalysis(**cached_analysis)
            logger.info("Using cached analysis")
        else:
            analysis = await loop.run_in_executor(
                None, analyzer.analyze_transcription, transcription, metadata.title
            )
            cache.set_video_analysis(metadata.video_id, analysis.dict())

        await _progress("analyzing", 100, "Analysis complete")

        # ── Step 4: Score & select moments ────────────────────────────────────
        processing_jobs[job_id]["status"] = "scoring"
        scored_moments = scorer.score_moments(transcription, analysis)
        filtered_moments = scorer.filter_overlapping_moments(scored_moments)
        top_moments = filtered_moments[: clip_settings.num_clips]
        await _progress(
            "detecting", 100,
            f"Identified {len(top_moments)} viral moment(s)",
        )

        # ── Step 5: Render clips in parallel ─────────────────────────────────
        processing_jobs[job_id]["status"] = "editing"
        total = len(top_moments)
        done_count = [0]  # mutable counter shared with callbacks
        generated_clips: list[Clip] = []

        def _render_clip(idx: int, moment) -> Optional[Clip]:
            clip_start = moment.timestamp
            clip_end = min(clip_start + clip_settings.clip_duration, transcription.duration)

            clip_segments = [
                seg for seg in transcription.segments
                if seg.start >= clip_start and seg.end <= clip_end
            ]
            clip_transcription = Transcription(
                text=" ".join(s.text for s in clip_segments),
                segments=clip_segments,
                language=transcription.language,
                duration=clip_end - clip_start,
            )

            try:
                final_clip_path = editor.process_clip(
                    video_path,
                    clip_start,
                    clip_end,
                    transcription=clip_transcription,
                    settings_obj=clip_settings,
                    add_subtitles=True,
                )
                thumbnail_path = editor.generate_thumbnail(
                    final_clip_path,
                    clip_start + (clip_end - clip_start) / 2,
                )
                reasons = getattr(moment, "top_reasons", []) or [getattr(moment, "reason", "")]
                return Clip(
                    id=f"{job_id}_clip_{idx}",
                    video_id=metadata.video_id,
                    start_time=clip_start,
                    end_time=clip_end,
                    duration=clip_end - clip_start,
                    score=getattr(moment, "overall_score", 0) or getattr(moment, "score", 0),
                    title=f"Clip {idx + 1}: {reasons[0] if reasons else 'Great moment'}",
                    description="\n".join(reasons),
                    video_path=final_clip_path,
                    thumbnail_path=thumbnail_path,
                    transcription=clip_transcription.text,
                    enabled=True,
                    status="ready",
                )
            except Exception as exc:
                logger.error(f"Clip {idx} render failed: {exc}")
                return None

        # Run renders concurrently (I/O-bound FFmpeg subprocess)
        futures = [
            loop.run_in_executor(None, _render_clip, idx, moment)
            for idx, moment in enumerate(top_moments)
        ]

        for coro in asyncio.as_completed(futures):
            clip: Optional[Clip] = await coro
            done_count[0] += 1
            pct = int(done_count[0] * 100 / total)
            if clip is not None:
                generated_clips.append(clip)
                await broadcast_clip_generated(job_id, clip)
            await _progress(
                "editing", pct,
                f"Rendered {done_count[0]}/{total} clip(s)…",
                current_clip=done_count[0],
                total_clips=total,
            )

        # Sort by score descending so frontend receives them ranked
        generated_clips.sort(
            key=lambda c: getattr(c, "score", 0), reverse=True
        )

        processing_jobs[job_id]["status"] = "completed"
        processing_jobs[job_id]["clips"] = [c.dict() for c in generated_clips]
        processing_jobs[job_id]["progress"] = 100
        await broadcast_complete(job_id, generated_clips)
        logger.info(f"Job {job_id} done: {len(generated_clips)}/{total} clip(s)")

    except Exception as exc:
        logger.exception(f"Job {job_id} failed")
        await _error(str(exc))


async def export_clips_job(job_id: str, request: ClipExport):
    """Export selected clips"""
    try:
        logger.info(f"Exporting clips for job {job_id}: {request.clip_ids}")

        exported_clips = []
        total_size = 0

        for clip_id in request.clip_ids:
            # Find clip (in production, query from database)
            # For now, check processing jobs
            for job_data in processing_jobs.values():
                clips = job_data.get("clips", [])
                clip = next((c for c in clips if c["id"] == clip_id), None)

                if clip and clip.get("video_path"):
                    if os.path.exists(clip["video_path"]):
                        file_size = os.path.getsize(clip["video_path"])
                        total_size += file_size
                        exported_clips.append(clip["video_path"])

        result = ExportResult(
            success=len(exported_clips) > 0,
            exported_clips=exported_clips,
            total_size_mb=round(total_size / (1024 * 1024), 2),
            export_path=settings.PROCESSED_DIR
        )

        # Send completion notification
        message = {
            "type": "export_complete",
            "job_id": job_id,
            "data": result.dict()
        }

        for connection in active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass

        logger.info(f"Export complete: {len(exported_clips)} clips")

    except Exception as e:
        logger.error(f"Export failed: {e}")


# Exception handlers
@app.exception_handler(AIClipperError)
async def ai_clipper_exception_handler(request, exc: AIClipperError):
    """Handle custom exceptions"""
    return JSONResponse(
        status_code=400,
        content={"error": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
