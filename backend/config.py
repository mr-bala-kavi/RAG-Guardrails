"""
Configuration settings for the RAG Guardrails application.
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
FAISS_DIR = DATA_DIR / "faiss_index"
LOGS_DIR = DATA_DIR / "logs"

# Create directories if they don't exist
for dir_path in [UPLOADS_DIR, FAISS_DIR, LOGS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Ollama settings
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3:mini")

# Embedding model settings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384  # Dimension for all-MiniLM-L6-v2

# Document processing settings
CHUNK_SIZE = 500  # characters
CHUNK_OVERLAP = 50  # characters
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# Retrieval settings
TOP_K_RESULTS = 10
SIMILARITY_THRESHOLD = 0.3

# Guardrail settings
TRUST_SCORE_THRESHOLD = 0.6
MAX_CONTEXT_LENGTH = 2000  # characters for low trust
MAX_CONTEXT_LENGTH_HIGH_TRUST = 4000  # characters for high trust

# Allowed file extensions
ALLOWED_EXTENSIONS = {".pdf", ".txt"}
