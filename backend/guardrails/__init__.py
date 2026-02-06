"""
Guardrails module for securing RAG pipeline.
"""
from .input_guard import InputGuard, InputCheckResult
from .document_sanitizer import DocumentSanitizer
from .system_prompt import SystemPromptManager
from .trust_scorer import TrustScorer
from .output_guard import OutputGuard, OutputCheckResult
from .logger import SecurityLogger

__all__ = [
    "InputGuard",
    "InputCheckResult", 
    "DocumentSanitizer",
    "SystemPromptManager",
    "TrustScorer",
    "OutputGuard",
    "OutputCheckResult",
    "SecurityLogger"
]


class GuardrailsManager:
    """Convenience class that holds all guardrail components."""
    
    def __init__(self):
        self.input_guard = InputGuard()
        self.doc_sanitizer = DocumentSanitizer()
        self.prompt_manager = SystemPromptManager()
        self.trust_scorer = TrustScorer()
        self.output_guard = OutputGuard()
        self.logger = SecurityLogger()
