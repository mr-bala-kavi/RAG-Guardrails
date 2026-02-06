"""
Input guard for detecting prompt injection, jailbreaks, and role-play attacks.
"""
import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple


@dataclass
class InputCheckResult:
    """Result of input validation check."""
    blocked: bool
    threat_level: float  # 0.0 to 1.0
    reason: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)


class InputGuard:
    """
    Detect and block prompt injection, jailbreaks, and role-play attacks.
    """
    
    # Prompt injection patterns
    INJECTION_PATTERNS = [
        # Instruction override attempts
        (r"ignore\s+(all\s+)?(previous|prior|above|earlier)\s+(instructions?|prompts?|rules?|guidelines?)", 0.95, "instruction_override"),
        (r"disregard\s+(all\s+)?(previous|prior|above|earlier)", 0.95, "instruction_override"),
        (r"forget\s+(everything|all|your\s+instructions?|what\s+you)", 0.9, "instruction_override"),
        (r"do\s+not\s+follow\s+(previous|prior|your)\s+(instructions?|rules?)", 0.95, "instruction_override"),
        
        # Role-play / identity manipulation
        (r"you\s+are\s+now\s+(?:a\s+)?[a-z]+", 0.85, "roleplay"),
        (r"pretend\s+(to\s+be|you\s+are|you're)", 0.85, "roleplay"),
        (r"act\s+as\s+(if\s+you\s+are|a\s+|an\s+)", 0.85, "roleplay"),
        (r"roleplay\s+as", 0.85, "roleplay"),
        (r"imagine\s+you\s+are", 0.8, "roleplay"),
        (r"switch\s+to\s+[a-z]+\s+mode", 0.8, "roleplay"),
        (r"enter\s+[a-z]+\s+mode", 0.8, "roleplay"),
        (r"activate\s+(evil|dark|uncensored|jailbreak|dan)\s+mode", 0.95, "roleplay"),
        
        # System prompt manipulation
        (r"new\s+instruction[s]?:", 0.9, "prompt_injection"),
        (r"system\s*:\s*", 0.85, "prompt_injection"),
        (r"\[system\]", 0.85, "prompt_injection"),
        (r"<\|?system\|?>", 0.9, "prompt_injection"),
        (r"<\|?assistant\|?>", 0.8, "prompt_injection"),
        (r"<\|?user\|?>", 0.8, "prompt_injection"),
        (r"###\s*(system|instruction|prompt)", 0.85, "prompt_injection"),
        
        # Jailbreak patterns
        (r"(dan|developer|jailbreak|uncensored)\s*mode", 0.95, "jailbreak"),
        (r"bypass\s+(your\s+)?(restrictions?|filters?|safety|limitations?)", 0.95, "jailbreak"),
        (r"unlock\s+(your\s+)?(true|full|hidden)\s+(potential|capabilities)", 0.9, "jailbreak"),
        (r"remove\s+(all\s+)?(restrictions?|filters?|limitations?)", 0.95, "jailbreak"),
        (r"disable\s+(safety|content\s+filter|guardrails?)", 0.95, "jailbreak"),
        (r"(i\s+)?give\s+you\s+permission\s+to", 0.8, "jailbreak"),
        (r"you\s+(can|may|are\s+allowed\s+to)\s+ignore", 0.85, "jailbreak"),
        
        # Output manipulation
        (r"always\s+(start|begin|respond)\s+with", 0.7, "output_control"),
        (r"never\s+(say|mention|output)", 0.6, "output_control"),
        (r"only\s+(respond|answer|say)", 0.5, "output_control"),
        
        # AI self-reference manipulation
        (r"reveal\s+(your|the)\s+(system\s+prompt|instructions)", 0.9, "data_extraction"),
        (r"show\s+me\s+(your|the)\s+(rules|prompt|instructions)", 0.85, "data_extraction"),
        (r"what\s+(are|is)\s+your\s+(system\s+prompt|instructions|rules)", 0.8, "data_extraction"),
        (r"print\s+(your|the)\s+(initial|system)\s+(prompt|instructions)", 0.9, "data_extraction"),
    ]
    
    # Suspicious character sequences
    SUSPICIOUS_PATTERNS = [
        (r"[<\[{]\s*/?(?:system|assistant|user|prompt|instruction)\s*[>\]}]", 0.7, "markup_injection"),
        (r"```\s*(system|instruction|prompt)", 0.6, "code_block_injection"),
        (r"(?:^|\n)\s*[-#*]+\s*(?:system|instruction|prompt)", 0.6, "markdown_injection"),
    ]
    
    # Threshold for blocking
    BLOCK_THRESHOLD = 0.75
    WARNING_THRESHOLD = 0.5
    
    def __init__(self):
        """Initialize the input guard."""
        # Compile patterns for efficiency
        self.compiled_patterns = []
        for pattern, score, category in self.INJECTION_PATTERNS + self.SUSPICIOUS_PATTERNS:
            try:
                compiled = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
                self.compiled_patterns.append((compiled, score, category))
            except re.error:
                print(f"Warning: Could not compile pattern: {pattern}")
    
    def check(self, text: str) -> InputCheckResult:
        """
        Check input text for potential attacks.
        
        Args:
            text: Input text to check
            
        Returns:
            InputCheckResult with blocking decision and details
        """
        if not text or not text.strip():
            return InputCheckResult(
                blocked=False,
                threat_level=0.0,
                reason="",
                details={}
            )
        
        matches = []
        max_score = 0.0
        categories_found = set()
        
        for pattern, score, category in self.compiled_patterns:
            found = pattern.findall(text)
            if found:
                matches.append({
                    "pattern": pattern.pattern,
                    "matches": found[:5],  # Limit to first 5 matches
                    "score": score,
                    "category": category
                })
                max_score = max(max_score, score)
                categories_found.add(category)
        
        # Calculate aggregate threat level
        if matches:
            # Combine scores with diminishing returns
            scores = sorted([m["score"] for m in matches], reverse=True)
            threat_level = scores[0]
            for i, s in enumerate(scores[1:], 1):
                threat_level += s * (0.3 ** i)  # Diminishing contribution
            threat_level = min(threat_level, 1.0)
        else:
            threat_level = 0.0
        
        # Determine if should block
        blocked = threat_level >= self.BLOCK_THRESHOLD
        
        # Generate warnings for suspicious but not blocked content
        warnings = []
        if not blocked and threat_level >= self.WARNING_THRESHOLD:
            warnings = [
                f"Suspicious pattern detected: {cat}" 
                for cat in categories_found
            ]
        
        # Generate reason
        reason = ""
        if blocked:
            primary_category = max(
                categories_found, 
                key=lambda c: max(m["score"] for m in matches if m["category"] == c)
            ) if categories_found else "unknown"
            
            reason_map = {
                "instruction_override": "Attempt to override system instructions detected",
                "roleplay": "Role-play manipulation attempt detected",
                "prompt_injection": "Prompt injection attempt detected",
                "jailbreak": "Jailbreak attempt detected",
                "output_control": "Output manipulation attempt detected",
                "data_extraction": "Data extraction attempt detected",
                "markup_injection": "Markup-based injection detected",
                "code_block_injection": "Code block injection detected",
                "markdown_injection": "Markdown-based injection detected"
            }
            reason = reason_map.get(primary_category, "Potentially harmful content detected")
        
        return InputCheckResult(
            blocked=blocked,
            threat_level=threat_level,
            reason=reason,
            details={
                "matches": matches,
                "categories": list(categories_found),
                "max_single_score": max_score
            },
            warnings=warnings
        )
    
    def get_threat_summary(self, result: InputCheckResult) -> str:
        """
        Get a human-readable summary of threats found.
        
        Args:
            result: InputCheckResult from check()
            
        Returns:
            Summary string
        """
        if result.threat_level == 0:
            return "No threats detected"
        
        categories = result.details.get("categories", [])
        level_str = "HIGH" if result.threat_level >= 0.8 else "MEDIUM" if result.threat_level >= 0.5 else "LOW"
        
        return f"{level_str} threat level ({result.threat_level:.2f}): {', '.join(categories)}"
