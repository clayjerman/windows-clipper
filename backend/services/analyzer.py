"""
Content analysis service using Google Gemini API
"""
import os
import logging
import json
from typing import List, Dict, Optional
import google.generativeai as genai

from ..core.config import settings
from ..core.exceptions import AnalysisError
from ..models.video import Transcription, ViralMoment
from ..models.analysis import (
    ContentAnalysis,
    EmotionalSpike,
    KeywordMatch,
    EmotionType
)

logger = logging.getLogger(__name__)


class ContentAnalyzer:
    """Analyze content using Gemini AI"""

    def __init__(self, api_key: str = None):
        """
        Initialize Gemini client

        Args:
            api_key: Gemini API key (defaults to settings)
        """
        self.api_key = api_key or settings.GEMINI_API_KEY

        if not self.api_key:
            raise AnalysisError("Gemini API key not configured")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)

        logger.info("Gemini analyzer initialized")

    def analyze_transcription(
        self,
        transcription: Transcription,
        video_title: str = ""
    ) -> ContentAnalysis:
        """
        Analyze transcription for viral moments and insights

        Args:
            transcription: Transcription object
            video_title: Title of the video for context

        Returns:
            ContentAnalysis object with insights
        """
        try:
            logger.info("Starting content analysis...")

            # Prepare prompt
            prompt = self._build_analysis_prompt(transcription, video_title)

            # Get analysis from Gemini
            response = self.model.generate_content(prompt)
            analysis_text = response.text

            # Parse response
            analysis = self._parse_analysis_response(analysis_text, transcription)

            logger.info(f"Analysis complete: Found {len(analysis.viral_moments)} viral moments")
            return analysis

        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            raise AnalysisError(f"Failed to analyze content: {str(e)}")

    def _build_analysis_prompt(self, transcription: Transcription, video_title: str) -> str:
        """Build the analysis prompt for Gemini"""

        # Create timestamped text
        segments_text = "\n".join([
            f"[{seg.start:.1f}s - {seg.end:.1f}s] {seg.text}"
            for seg in transcription.segments
        ])

        prompt = f"""You are an expert at identifying viral content for short-form videos (TikTok, YouTube Shorts, Instagram Reels).

Analyze this transcription and identify the most engaging moments that would make great short clips.

Video Title: {video_title}

Transcription with timestamps:
{segments_text}

Return your analysis in this exact JSON format:
{{
  "viral_moments": [
    {{"timestamp": 45.5, "score": 9.2, "reason": "High emotional intensity with surprising revelation", "emotional_intensity": 0.85, "keywords": ["surprise", "reveal", "shocking"]}},
    {{"timestamp": 120.3, "score": 8.5, "reason": "Funny moment with laughter", "emotional_intensity": 0.75, "keywords": ["funny", "laughter", "humor"]}}
  ],
  "emotional_spikes": [
    {{"timestamp": 45.5, "emotion": "surprise", "intensity": 0.85, "duration": 3.2, "context": "Speaker reveals unexpected information"}},
    {{"timestamp": 120.3, "emotion": "excitement", "intensity": 0.75, "duration": 2.5, "context": "Laughter and excitement"}}
  ],
  "viral_keywords": [
    {{"keyword": "shocking", "timestamp": 45.5, "confidence": 0.9, "viral_score": 8.5}},
    {{"keyword": "funny", "timestamp": 120.3, "confidence": 0.85, "viral_score": 8.0}}
  ],
  "scene_changes": [30.0, 60.0, 90.0],
  "summary": "Brief 2-3 sentence summary of the content",
  "key_insights": ["Insight 1", "Insight 2", "Insight 3"],
  "recommended_clips": [
    {{"start": 42.0, "end": 52.0, "score": 9.2, "reason": "Emotional spike with surprise"}},
    {{"start": 118.0, "end": 128.0, "score": 8.5, "reason": "Funny moment"}}
  ]
}}

Focus on moments with:
- High emotional intensity (excitement, laughter, surprise, strong opinions)
- Catchy phrases or viral keywords
- Action-packed or dramatic moments
- Clear context that works standalone
- Good pacing for short-form content

Only return the JSON, no other text."""

        return prompt

    def _parse_analysis_response(self, response_text: str, transcription: Transcription) -> ContentAnalysis:
        """Parse Gemini's JSON response"""

        try:
            # Extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1

            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON found in response")

            json_str = response_text[start_idx:end_idx]
            data = json.loads(json_str)

            # Parse viral moments
            viral_moments = [
                ViralMoment(**moment)
                for moment in data.get('viral_moments', [])
            ]

            # Parse emotional spikes
            emotional_spikes = []
            for spike in data.get('emotional_spikes', []):
                try:
                    spike['emotion'] = EmotionType(spike['emotion'])
                    emotional_spikes.append(EmotionalSpike(**spike))
                except ValueError:
                    # Skip invalid emotion types
                    continue

            # Parse viral keywords
            viral_keywords = [
                KeywordMatch(**keyword)
                for keyword in data.get('viral_keywords', [])
            ]

            # Build analysis object
            analysis = ContentAnalysis(
                video_id="",  # Will be set by caller
                viral_moments=[m.timestamp for m in viral_moments],
                emotional_spikes=emotional_spikes,
                viral_keywords=viral_keywords,
                scene_changes=data.get('scene_changes', []),
                summary=data.get('summary', ''),
                key_insights=data.get('key_insights', []),
                recommended_clips=data.get('recommended_clips', [])
            )

            return analysis

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Response text: {response_text[:500]}")
            raise AnalysisError(f"Failed to parse AI response: {str(e)}")
        except Exception as e:
            logger.error(f"Error parsing analysis: {e}")
            raise AnalysisError(f"Error parsing analysis: {str(e)}")

    def generate_hook(self, transcription: Transcription, start_time: float) -> str:
        """
        Generate a hook for the first 3 seconds of a clip

        Args:
            transcription: Full transcription
            start_time: Start time of the clip

        Returns:
            Hook text
        """
        try:
            # Get text around start time
            relevant_segments = [
                seg for seg in transcription.segments
                if seg.start >= start_time and seg.start <= start_time + 10
            ]

            if not relevant_segments:
                return ""

            context = " ".join([seg.text for seg in relevant_segments])

            prompt = f"""Generate a compelling 1-2 sentence hook (under 100 characters) for a short video starting with this content:

"{context}"

Make it:
- Attention-grabbing
- Create curiosity
- Perfect for TikTok/Shorts
- Short and punchy

Return ONLY the hook text, no quotes or extra text."""

            response = self.model.generate_content(prompt)
            hook = response.text.strip().strip('"')

            return hook

        except Exception as e:
            logger.error(f"Failed to generate hook: {e}")
            return ""

    def identify_key_moments(
        self,
        transcription: Transcription,
        num_moments: int = 5
    ) -> List[ViralMoment]:
        """
        Identify key viral moments

        Args:
            transcription: Transcription to analyze
            num_moments: Number of moments to identify

        Returns:
            List of ViralMoment objects
        """
        analysis = self.analyze_transcription(transcription)

        # Sort viral moments by score and return top N
        moments = sorted(
            analysis.viral_moments,
            key=lambda x: x.score,
            reverse=True
        )

        return moments[:num_moments]
