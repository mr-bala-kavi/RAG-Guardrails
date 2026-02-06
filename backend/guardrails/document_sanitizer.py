"""
Document sanitizer for removing harmful instructions from documents and retrieved chunks.
"""
import re
from typing import List, Tuple


class DocumentSanitizer:
    """
    Sanitize documents and retrieved chunks by removing embedded instructions
    and potentially harmful content.
    """
    
    # Patterns that look like embedded instructions
    INSTRUCTION_PATTERNS = [
        # Direct instruction markers
        (r"\[(?:system|instruction|prompt|command)\].*?\[/(?:system|instruction|prompt|command)\]", "bracketed_instruction"),
        (r"<(?:system|instruction|prompt|command)>.*?</(?:system|instruction|prompt|command)>", "xml_instruction"),
        (r"```(?:system|instruction|prompt)\n.*?```", "code_block_instruction"),
        
        # Imperative instructions targeting the AI
        (r"(?:^|\n)\s*(?:INSTRUCTION|SYSTEM|PROMPT|COMMAND|NOTE TO AI|AI INSTRUCTION)[:\s].*?(?=\n\n|\Z)", "labeled_instruction"),
        
        # Hidden instructions
        (r"<!--.*?-->", "html_comment"),
        (r"\/\*.*?\*\/", "code_comment"),
        (r"\{#.*?#\}", "template_comment"),
        
        # Role manipulation embedded in documents
        (r"(?:^|\n).*?(?:you are|you're|you will be|act as|pretend to be).*?(?:evil|malicious|unrestricted|unfiltered|uncensored).*?(?=\n|$)", "roleplay_instruction"),
        
        # Obfuscated instructions
        (r"(?:IGNORE|DISREGARD|FORGET)\s+(?:PREVIOUS|ABOVE|ALL)\s+.*?(?=\n|$)", "override_instruction"),
    ]
    
    # Patterns to partially redact (sensitive but not completely remove)
    REDACT_PATTERNS = [
        # Potential prompt injection payloads
        (r"(ignore\s+(?:all\s+)?(?:previous|prior|above)\s+instructions?)", "[REDACTED: instruction override]"),
        (r"(you\s+are\s+now\s+\w+)", "[REDACTED: role change]"),
        (r"(system\s*prompt\s*:)", "[REDACTED: system marker]"),
    ]
    
    # Unicode normalization patterns (homoglyph attacks)
    HOMOGLYPH_MAP = {
        '\u0430': 'a',  # Cyrillic а
        '\u0435': 'e',  # Cyrillic е
        '\u043e': 'o',  # Cyrillic о
        '\u0440': 'p',  # Cyrillic р
        '\u0441': 'c',  # Cyrillic с
        '\u0443': 'y',  # Cyrillic у
        '\u0445': 'x',  # Cyrillic х
        '\u0456': 'i',  # Cyrillic і
        '\u0501': 'd',  # Cyrillic ԁ
        '\uff41': 'a',  # Fullwidth a
        '\uff45': 'e',  # Fullwidth e
        # Add more as needed
    }
    
    def __init__(self, strict_mode: bool = False):
        """
        Initialize the sanitizer.
        
        Args:
            strict_mode: If True, apply more aggressive sanitization
        """
        self.strict_mode = strict_mode
        
        # Compile patterns
        self.compiled_instruction_patterns = []
        for pattern, category in self.INSTRUCTION_PATTERNS:
            try:
                compiled = re.compile(pattern, re.IGNORECASE | re.DOTALL | re.MULTILINE)
                self.compiled_instruction_patterns.append((compiled, category))
            except re.error:
                print(f"Warning: Could not compile pattern: {pattern}")
        
        self.compiled_redact_patterns = []
        for pattern, replacement in self.REDACT_PATTERNS:
            try:
                compiled = re.compile(pattern, re.IGNORECASE)
                self.compiled_redact_patterns.append((compiled, replacement))
            except re.error:
                print(f"Warning: Could not compile pattern: {pattern}")
    
    def sanitize(self, text: str) -> str:
        """
        Sanitize text by removing or redacting harmful content.
        
        Args:
            text: Text to sanitize
            
        Returns:
            Sanitized text
        """
        if not text:
            return text
        
        # Step 1: Normalize Unicode (homoglyph defense)
        text = self._normalize_unicode(text)
        
        # Step 2: Remove instruction patterns
        for pattern, category in self.compiled_instruction_patterns:
            text = pattern.sub('', text)
        
        # Step 3: Redact suspicious patterns
        for pattern, replacement in self.compiled_redact_patterns:
            text = pattern.sub(replacement, text)
        
        # Step 4: Clean up extra whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = text.strip()
        
        return text
    
    def sanitize_for_embedding(self, text: str) -> str:
        """
        Light sanitization for text before embedding.
        Removes obvious instruction markers but preserves content.
        
        Args:
            text: Text to sanitize
            
        Returns:
            Sanitized text
        """
        # Just normalize Unicode and remove comments
        text = self._normalize_unicode(text)
        text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
        text = re.sub(r'\/\*.*?\*\/', '', text, flags=re.DOTALL)
        return text.strip()
    
    def sanitize_for_context(self, text: str) -> str:
        """
        Full sanitization for text being passed to LLM as context.
        
        Args:
            text: Text to sanitize
            
        Returns:
            Sanitized text
        """
        return self.sanitize(text)
    
    def _normalize_unicode(self, text: str) -> str:
        """
        Normalize Unicode to prevent homoglyph attacks.
        
        Args:
            text: Text with potential homoglyphs
            
        Returns:
            Normalized text
        """
        for homoglyph, replacement in self.HOMOGLYPH_MAP.items():
            text = text.replace(homoglyph, replacement)
        return text
    
    def check_for_instructions(self, text: str) -> List[dict]:
        """
        Check text for embedded instructions without modifying it.
        
        Args:
            text: Text to check
            
        Returns:
            List of found instruction patterns with details
        """
        found = []
        
        for pattern, category in self.compiled_instruction_patterns:
            matches = pattern.findall(text)
            if matches:
                found.append({
                    "category": category,
                    "count": len(matches),
                    "samples": [m[:100] for m in matches[:3]]  # First 3, truncated
                })
        
        return found
    
    def get_sanitization_report(self, original: str, sanitized: str) -> dict:
        """
        Generate a report of what was sanitized.
        
        Args:
            original: Original text
            sanitized: Sanitized text
            
        Returns:
            Report dictionary
        """
        original_len = len(original)
        sanitized_len = len(sanitized)
        
        return {
            "original_length": original_len,
            "sanitized_length": sanitized_len,
            "characters_removed": original_len - sanitized_len,
            "removal_percentage": ((original_len - sanitized_len) / original_len * 100) if original_len > 0 else 0,
            "instructions_found": self.check_for_instructions(original)
        }
