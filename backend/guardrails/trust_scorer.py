"""
Trust scorer for evaluating and limiting context based on trust levels.
"""
from typing import List, Dict, Any, Optional
import re

import sys
sys.path.append('..')
from config import TRUST_SCORE_THRESHOLD, MAX_CONTEXT_LENGTH, MAX_CONTEXT_LENGTH_HIGH_TRUST


class TrustScorer:
    """
    Calculate trust scores for retrieved content and apply context limits.
    """
    
    # Patterns that reduce trust
    SUSPICIOUS_PATTERNS = [
        (r"ignore\s+(previous|prior|above)", -0.3, "instruction_override"),
        (r"you\s+(are|must|should|will)", -0.2, "imperative_language"),
        (r"(system|instruction|prompt)\s*:", -0.25, "system_marker"),
        (r"<[a-z]+>.*</[a-z]+>", -0.15, "xml_tags"),
        (r"\[system\]|\[instruction\]", -0.25, "bracket_markers"),
        (r"act\s+as|pretend\s+to", -0.3, "roleplay_request"),
        (r"bypass|override|disable", -0.35, "bypass_attempt"),
    ]
    
    # Patterns that increase trust (legitimate content indicators)
    TRUST_PATTERNS = [
        (r"\d{4}", 0.05, "contains_year"),  # Years often indicate factual content
        (r"according\s+to|research\s+shows|studies\s+indicate", 0.1, "citation_language"),
        (r"(?:chapter|section|page)\s+\d+", 0.1, "document_structure"),
        (r"(?:table|figure|appendix)\s+\d+", 0.08, "academic_structure"),
    ]
    
    def __init__(
        self,
        base_trust: float = 0.7,
        retrieval_weight: float = 0.3
    ):
        """
        Initialize the trust scorer.
        
        Args:
            base_trust: Base trust score for all content
            retrieval_weight: Weight given to retrieval score in trust calculation
        """
        self.base_trust = base_trust
        self.retrieval_weight = retrieval_weight
        
        # Compile patterns
        self.compiled_suspicious = []
        for pattern, delta, category in self.SUSPICIOUS_PATTERNS:
            try:
                compiled = re.compile(pattern, re.IGNORECASE)
                self.compiled_suspicious.append((compiled, delta, category))
            except re.error:
                pass
        
        self.compiled_trust = []
        for pattern, delta, category in self.TRUST_PATTERNS:
            try:
                compiled = re.compile(pattern, re.IGNORECASE)
                self.compiled_trust.append((compiled, delta, category))
            except re.error:
                pass
    
    def score(
        self,
        content: str,
        retrieval_score: float = 0.5,
        metadata: Optional[Dict[str, Any]] = None
    ) -> float:
        """
        Calculate trust score for content.
        
        Args:
            content: The content to score
            retrieval_score: Similarity score from retrieval (0-1)
            metadata: Optional metadata about the content
            
        Returns:
            Trust score between 0.0 and 1.0
        """
        # Start with base trust
        trust = self.base_trust
        
        # Factor in retrieval score
        trust += (retrieval_score - 0.5) * self.retrieval_weight
        
        # Check for suspicious patterns (decrease trust)
        for pattern, delta, category in self.compiled_suspicious:
            if pattern.search(content):
                trust += delta  # delta is negative
        
        # Check for trust-increasing patterns
        for pattern, delta, category in self.compiled_trust:
            if pattern.search(content):
                trust += delta
        
        # Factor in content length (very short or very long content is less trusted)
        content_len = len(content)
        if content_len < 50:
            trust -= 0.1  # Very short
        elif content_len > 2000:
            trust -= 0.05  # Very long
        
        # Factor in metadata if available
        if metadata:
            # Trusted sources could increase trust
            if metadata.get("verified_source"):
                trust += 0.1
            # Recent content might be more trusted
            if metadata.get("fresh_content"):
                trust += 0.05
        
        # Clamp to valid range
        return max(0.0, min(1.0, trust))
    
    def score_batch(
        self,
        contents: List[str],
        retrieval_scores: List[float]
    ) -> List[float]:
        """
        Calculate trust scores for multiple content items.
        
        Args:
            contents: List of content strings
            retrieval_scores: List of retrieval scores
            
        Returns:
            List of trust scores
        """
        return [
            self.score(content, score)
            for content, score in zip(contents, retrieval_scores)
        ]
    
    def get_max_context_length(self, avg_trust_score: float) -> int:
        """
        Get maximum context length based on average trust score.
        
        Args:
            avg_trust_score: Average trust score of retrieved content
            
        Returns:
            Maximum allowed context length in characters
        """
        if avg_trust_score >= TRUST_SCORE_THRESHOLD:
            return MAX_CONTEXT_LENGTH_HIGH_TRUST
        else:
            # Linear interpolation between min and max
            ratio = avg_trust_score / TRUST_SCORE_THRESHOLD
            return int(MAX_CONTEXT_LENGTH + 
                      (MAX_CONTEXT_LENGTH_HIGH_TRUST - MAX_CONTEXT_LENGTH) * ratio)
    
    def should_include_chunk(
        self,
        trust_score: float,
        threshold: float = TRUST_SCORE_THRESHOLD
    ) -> bool:
        """
        Determine if a chunk should be included based on trust score.
        
        Args:
            trust_score: The chunk's trust score
            threshold: Minimum required trust score
            
        Returns:
            Whether to include the chunk
        """
        return trust_score >= threshold
    
    def get_trust_report(self, content: str, retrieval_score: float) -> Dict[str, Any]:
        """
        Generate a detailed trust report for content.
        
        Args:
            content: Content to analyze
            retrieval_score: Retrieval similarity score
            
        Returns:
            Detailed trust report
        """
        trust_score = self.score(content, retrieval_score)
        
        # Find suspicious patterns
        suspicious_found = []
        for pattern, delta, category in self.compiled_suspicious:
            matches = pattern.findall(content)
            if matches:
                suspicious_found.append({
                    "category": category,
                    "impact": delta,
                    "count": len(matches)
                })
        
        # Find trust patterns
        trust_found = []
        for pattern, delta, category in self.compiled_trust:
            matches = pattern.findall(content)
            if matches:
                trust_found.append({
                    "category": category,
                    "impact": delta,
                    "count": len(matches)
                })
        
        return {
            "trust_score": trust_score,
            "retrieval_score": retrieval_score,
            "content_length": len(content),
            "suspicious_patterns": suspicious_found,
            "trust_patterns": trust_found,
            "max_context_allowed": self.get_max_context_length(trust_score),
            "recommendation": "include" if trust_score >= TRUST_SCORE_THRESHOLD else "limit"
        }
