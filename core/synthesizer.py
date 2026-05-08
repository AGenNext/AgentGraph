"""Result synthesizer for multi-agent outputs."""

from typing import Optional
from dataclasses import dataclass

from agents.base_agent import ContentResult


@dataclass
class SynthesisResult:
    """Result of synthesizer."""
    
    content: str
    sources: dict[str, str]
    quality_score: float
    synthesis_method: str


class ResultSynthesizer:
    """Synthesizes results from multiple agents."""
    
    def __init__(self):
        self.default_method = "best_first"
    
    def synthesize(
        self,
        results: list[ContentResult],
        method: str = "best_first",
    ) -> SynthesisResult:
        """Synthesize results using specified method."""
        
        if not results:
            return SynthesisResult(
                content="",
                sources={},
                quality_score=0.0,
                synthesis_method=method,
            )
        
        if method == "best_first":
            return self._synthesize_best_first(results)
        elif method == "combine":
            return self._synthesize_combine(results)
        elif method == "ranked":
            return self._synthesize_ranked(results)
        else:
            return self._synthesize_best_first(results)
    
    def _synthesize_best_first(
        self,
        results: list[ContentResult],
    ) -> SynthesisResult:
        """Use best result with annotations."""
        
        # Sort by quality
        sorted_results = sorted(
            results, 
            key=lambda r: r.quality_score, 
            reverse=True
        )
        
        best = sorted_results[0]
        
        # Build sources map
        sources = {
            r.agent_id: r.content[:200] + "..."
            for r in sorted_results
        }
        
        content = best.content + "\n\n---\n*Synthesized from multi-agent team*"
        
        return SynthesisResult(
            content=content,
            sources=sources,
            quality_score=best.quality_score * 1.05,  # Team bonus
            synthesis_method="best_first",
        )
    
    def _synthesize_combine(
        self,
        results: list[ContentResult],
    ) -> SynthesisResult:
        """Combine best elements from all results."""
        
        sorted_results = sorted(
            results,
            key=lambda r: r.quality_score,
            reverse=True,
        )
        
        best = sorted_results[0]
        
        sources = {
            r.agent_id: r.content[:100] + "..."
            for r in results
        }
        
        # Use best content
        content = best.content
        
        # Add sources note
        content += "\n\n---\n*Combined from sources: " + ", ".join(
            r.agent_id.split("-")[0] for r in results
        ) + "*"
        
        # Average quality with bonus
        avg_quality = sum(r.quality_score for r in results) / len(results)
        
        return SynthesisResult(
            content=content,
            sources=sources,
            quality_score=min(avg_quality * 1.1, 1.0),
            synthesis_method="combine",
        )
    
    def _synthesize_ranked(
        self,
        results: list[ContentResult],
    ) -> SynthesisResult:
        """Present ranked alternatives."""
        
        sorted_results = sorted(
            results,
            key=lambda r: r.quality_score,
            reverse=True,
        )
        
        sources = {
            r.agent_id: f"Score: {r.quality_score:.2f}"
            for r in sorted_results
        }
        
        # Build ranked content
        lines = ["# Ranked Results\n"]
        
        for i, r in enumerate(sorted_results, 1):
            lines.append(f"\n## Rank {i}: {r.agent_id.split('-')[0].title()}")
            lines.append(f"(Quality: {r.quality_score:.2f})")
            lines.append(r.content[:500] + "...")
        
        content = "\n".join(lines)
        
        return SynthesisResult(
            content=content,
            sources=sources,
            quality_score=sorted_results[0].quality_score,
            synthesis_method="ranked",
        )