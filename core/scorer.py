"""Quality scorer for agent outputs."""

from typing import Optional
from dataclasses import dataclass


@dataclass
class ScoreBreakdown:
    """Breakdown of quality scores."""
    
    overall: float
    relevance: float = 0.0
    originality: float = 0.0
    coherence: float = 0.0
    completeness: float = 0.0
    accuracy: float = 0.0


class QualityScorer:
    """Scores quality of agent-generated content."""
    
    # Weight for each metric
    WEIGHTS = {
        "relevance": 0.25,
        "originality": 0.20,
        "coherence": 0.20,
        "completeness": 0.20,
        "accuracy": 0.15,
    }
    
    def __init__(self):
        self._thresholds = {
            "excellent": 0.85,
            "good": 0.70,
            "acceptable": 0.50,
        }
    
    def score(self, content: str, topic: str) -> ScoreBreakdown:
        """Score content quality."""
        
        # Calculate individual metrics
        relevance = self._score_relevance(content, topic)
        originality = self._score_originality(content)
        coherence = self._score_coherence(content)
        completeness = self._score_completeness(content, topic)
        accuracy = self._score_accuracy(content)
        
        # Calculate weighted overall
        overall = (
            relevance * self.WEIGHTS["relevance"] +
            originality * self.WEIGHTS["originality"] +
            coherence * self.WEIGHTS["coherence"] +
            completeness * self.WEIGHTS["completeness"] +
            accuracy * self.WEIGHTS["accuracy"]
        )
        
        return ScoreBreakdown(
            overall=overall,
            relevance=relevance,
            originality=originality,
            coherence=coherence,
            completeness=completeness,
            accuracy=accuracy,
        )
    
    def _score_relevance(self, content: str, topic: str) -> float:
        """Score relevance to topic."""
        if not content or not topic:
            return 0.0
        
        # Simple keyword matching
        topic_words = topic.lower().split()
        content_lower = content.lower()
        
        matches = sum(1 for word in topic_words if word in content_lower)
        return min(matches / max(len(topic_words), 1), 1.0)
    
    def _score_originality(self, content: str) -> float:
        """Score originality (simple heuristic)."""
        if not content:
            return 0.0
        
        # Check for varied sentence structure
        sentences = content.split(".")
        unique_starts = len(set(s[:50] for s in sentences if len(s) > 10))
        
        return min(unique_starts / max(len(sentences), 1) + 0.3, 1.0)
    
    def _score_coherence(self, content: str) -> float:
        """Score coherence."""
        if not content:
            return 0.0
        
        # Check for basic structure (headers, paragraphs)
        has_headers = "#" in content or "##" in content
        has_paragraphs = "\n\n" in content
        
        score = 0.5
        if has_headers:
            score += 0.25
        if has_paragraphs:
            score += 0.25
        
        return min(score, 1.0)
    
    def _score_completeness(self, content: str, topic: str) -> float:
        """Score completeness."""
        if not content:
            return 0.0
        
        # Check length vs expected
        expected_length = 500  # Base expected length
        actual_length = len(content.split())
        
        length_ratio = actual_length / expected_length
        return min(max(length_ratio, 0.3), 1.5) / 1.5
    
    def _score_accuracy(self, content: str) -> float:
        """Score factual accuracy (placeholder)."""
        # In production, this would verify facts
        return 0.75
    
    def get_rating(self, score: float) -> str:
        """Get rating string from score."""
        if score >= self._thresholds["excellent"]:
            return "excellent"
        elif score >= self._thresholds["good"]:
            return "good"
        elif score >= self._thresholds["acceptable"]:
            return "acceptable"
        else:
            return "needs improvement"