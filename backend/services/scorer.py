"""
Viral moment scoring algorithm
"""
import logging
from typing import List, Dict, Tuple
import numpy as np

from ..models.video import Transcription
from ..models.analysis import (
    ContentAnalysis,
    ViralScoringCriteria,
    ViralScoreResult,
    EmotionType
)

logger = logging.getLogger(__name__)


class ViralScorer:
    """Score viral moments based on multiple factors"""

    def __init__(self, criteria: ViralScoringCriteria = None):
        """
        Initialize scorer with custom criteria

        Args:
            criteria: Scoring criteria (defaults to standard weights)
        """
        self.criteria = criteria or ViralScoringCriteria()

    def score_moments(
        self,
        transcription: Transcription,
        analysis: ContentAnalysis
    ) -> List[ViralScoreResult]:
        """
        Score all viral moments with detailed breakdown

        Args:
            transcription: Full transcription
            analysis: Content analysis from Gemini

        Returns:
            List of scored moments, sorted by score
        """
        scores = []

        # Score recommended clips from analysis
        for clip in analysis.recommended_clips:
            timestamp = clip.get('start', 0)
            result = self.score_single_moment(
                timestamp,
                transcription,
                analysis
            )
            scores.append(result)

        # Also score standalone viral moments
        for moment_timestamp in analysis.viral_moments:
            if not any(s.timestamp == moment_timestamp for s in scores):
                result = self.score_single_moment(
                    moment_timestamp,
                    transcription,
                    analysis
                )
                scores.append(result)

        # Sort by overall score
        scores.sort(key=lambda x: x.overall_score, reverse=True)

        logger.info(f"Scored {len(scores)} moments")
        return scores

    def score_single_moment(
        self,
        timestamp: float,
        transcription: Transcription,
        analysis: ContentAnalysis
    ) -> ViralScoreResult:
        """
        Score a single moment with detailed breakdown

        Args:
            timestamp: Moment timestamp in seconds
            transcription: Full transcription
            analysis: Content analysis

        Returns:
            ViralScoreResult with scores and reasons
        """
        # Get context (text around timestamp)
        context = self._get_context(transcription, timestamp, window=5)

        # Calculate individual scores
        emotional_score = self._score_emotional_intensity(timestamp, analysis)
        keyword_score = self._score_keywords(timestamp, context, analysis)
        speaker_score = self._score_speaker_engagement(context)
        pacing_score = self._score_pacing(transcription, timestamp)
        scene_score = self._score_scene_changes(timestamp, analysis)

        # Calculate weighted overall score
        overall_score = (
            emotional_score * self.criteria.emotional_weight +
            keyword_score * self.criteria.keyword_weight +
            speaker_score * self.criteria.speaker_weight +
            pacing_score * self.criteria.pacing_weight +
            scene_score * self.criteria.scene_weight
        )

        # Scale to 0-10
        overall_score = min(overall_score * 10, 10.0)

        # Generate reasons
        reasons = self._generate_reasons(
            emotional_score,
            keyword_score,
            speaker_score,
            pacing_score,
            scene_score,
            context
        )

        result = ViralScoreResult(
            timestamp=timestamp,
            overall_score=round(overall_score, 2),
            breakdown={
                'emotional': round(emotional_score * 10, 2),
                'keywords': round(keyword_score * 10, 2),
                'speaker': round(speaker_score * 10, 2),
                'pacing': round(pacing_score * 10, 2),
                'scene': round(scene_score * 10, 2)
            },
            top_reasons=reasons[:3]
        )

        return result

    def _get_context(self, transcription: Transcription, timestamp: float, window: float = 5) -> str:
        """Get text context around timestamp"""
        segments = [
            seg.text.strip()
            for seg in transcription.segments
            if abs(seg.start - timestamp) <= window
        ]
        return " ".join(segments)

    def _score_emotional_intensity(self, timestamp: float, analysis: ContentAnalysis) -> float:
        """Score based on emotional spikes (0-1)"""
        # Find nearest emotional spike
        spikes = analysis.emotional_spikes

        for spike in spikes:
            if abs(spike.timestamp - timestamp) <= 5:  # Within 5 seconds
                # Higher emotion intensity = higher score
                # Some emotions are more viral than others
                emotion_weights = {
                    EmotionType.EXCITEMENT: 1.2,
                    EmotionType.LAUGHTER: 1.3,
                    EmotionType.SURPRISE: 1.1,
                    EmotionType.ANGER: 1.0,
                    EmotionType.FEAR: 0.8,
                    EmotionType.SADNESS: 0.5,
                    EmotionType.NEUTRAL: 0.3
                }

                base_score = spike.intensity
                emotion_weight = emotion_weights.get(spike.emotion, 0.7)

                return min(base_score * emotion_weight, 1.0)

        return 0.3  # Baseline for no emotion detected

    def _score_keywords(self, timestamp: float, context: str, analysis: ContentAnalysis) -> float:
        """Score based on viral keywords (0-1)"""
        # Viral keywords/phrases for short-form content
        viral_keywords = [
            'shocking', 'amazing', 'incredible', 'crazy', 'insane',
            'secret', 'hidden', 'revealed', 'discovered', 'never',
            'hack', 'trick', 'tip', 'genius', 'brilliant',
            'must watch', 'you wont believe', 'this is why',
            'finally', 'game changer', 'revolutionary',
            'wait for it', 'plot twist', 'mind blown',
            'funny', 'hilarious', 'epic', 'legendary'
        ]

        context_lower = context.lower()

        # Check for viral keywords
        keyword_matches = sum(1 for kw in viral_keywords if kw in context_lower)

        # Check for Gemini-detected keywords
        for vk in analysis.viral_keywords:
            if abs(vk.timestamp - timestamp) <= 5:
                keyword_matches += 1

        # Score based on keyword density
        score = min(keyword_matches * 0.3, 1.0)

        return score

    def _score_speaker_engagement(self, context: str) -> float:
        """Score based on speaker engagement indicators (0-1)"""
        engagement_indicators = [
            '!', '?', 'listen', 'watch', 'look', 'see',
            'imagine', 'picture this', 'think about',
            'let me tell you', 'heres the thing',
            'the truth is', 'believe me', 'trust me'
        ]

        context_lower = context.lower()

        # Count engagement indicators
        engagement_count = sum(1 for ind in engagement_indicators if ind in context_lower)

        # Check for caps (emphasis)
        caps_ratio = sum(1 for c in context if c.isupper()) / max(len(context), 1)

        score = min(engagement_count * 0.15 + caps_ratio * 2, 1.0)

        return score

    def _score_pacing(self, transcription: Transcription, timestamp: float) -> float:
        """Score based on pacing and variation (0-1)"""
        # Get segments around timestamp
        segments = [
            seg for seg in transcription.segments
            if abs(seg.start - timestamp) <= 10
        ]

        if len(segments) < 2:
            return 0.5

        # Calculate variation in segment lengths
        durations = [seg.end - seg.start for seg in segments]
        duration_variance = np.var(durations)

        # Calculate words per second
        words_per_second = []
        for seg in segments:
            word_count = len(seg.text.split())
            duration = seg.end - seg.start
            if duration > 0:
                words_per_second.append(word_count / duration)

        avg_wps = np.mean(words_per_second) if words_per_second else 2.0

        # Optimal pacing for short-form: 2-3 words/second
        pacing_score = 1.0 - abs(avg_wps - 2.5) / 2.5

        # Some variation is good (but not too much)
        variance_score = min(duration_variance / 2.0, 1.0)

        return (pacing_score * 0.7 + variance_score * 0.3)

    def _score_scene_changes(self, timestamp: float, analysis: ContentAnalysis) -> float:
        """Score based on scene changes (0-1)"""
        # Find nearest scene changes
        scene_changes = analysis.scene_changes

        for sc in scene_changes:
            if abs(sc - timestamp) <= 3:  # Within 3 seconds
                return 0.8  # Scene changes are engaging

        return 0.4  # Baseline

    def _generate_reasons(
        self,
        emotional: float,
        keywords: float,
        speaker: float,
        pacing: float,
        scene: float,
        context: str
    ) -> List[str]:
        """Generate text explanations for scores"""
        reasons = []

        if emotional > 0.7:
            reasons.append("High emotional intensity detected")
        if keywords > 0.7:
            reasons.append("Contains viral keywords/phrases")
        if speaker > 0.7:
            reasons.append("Strong speaker engagement")
        if pacing > 0.7:
            reasons.append("Optimal pacing for short-form")
        if scene > 0.7:
            reasons.append("Engaging scene transition")

        # Fallback reasons
        if not reasons:
            reasons.append("Promising content moment")

        return reasons

    def filter_overlapping_moments(
        self,
        moments: List[ViralScoreResult],
        min_gap: float = 10.0
    ) -> List[ViralScoreResult]:
        """
        Filter out moments that are too close to each other

        Args:
            moments: List of scored moments
            min_gap: Minimum seconds between moments

        Returns:
            Filtered list
        """
        if not moments:
            return []

        filtered = [moments[0]]

        for moment in moments[1:]:
            last_timestamp = filtered[-1].timestamp

            if moment.timestamp - last_timestamp >= min_gap:
                filtered.append(moment)

        logger.info(f"Filtered {len(moments)} moments to {len(filtered)} non-overlapping")
        return filtered
