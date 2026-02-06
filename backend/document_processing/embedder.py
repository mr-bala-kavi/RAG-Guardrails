"""
Embedding model for generating vector representations of text.
"""
from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer

import sys
sys.path.append('..')
from config import EMBEDDING_MODEL


class EmbeddingModel:
    """Generate embeddings using sentence-transformers."""
    
    _instance = None
    _model = None
    
    def __new__(cls):
        """Singleton pattern to avoid loading model multiple times."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the embedding model."""
        if EmbeddingModel._model is None:
            print(f"Loading embedding model: {EMBEDDING_MODEL}")
            EmbeddingModel._model = SentenceTransformer(EMBEDDING_MODEL)
            print("Embedding model loaded successfully")
    
    @property
    def model(self) -> SentenceTransformer:
        """Get the loaded model."""
        return EmbeddingModel._model
    
    def embed(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Generate embeddings for text(s).
        
        Args:
            texts: Single text string or list of texts
            
        Returns:
            Numpy array of embeddings (n_texts, embedding_dim)
        """
        if isinstance(texts, str):
            texts = [texts]
        
        # Generate embeddings
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,  # L2 normalize for cosine similarity
            show_progress_bar=len(texts) > 10
        )
        
        return embeddings
    
    def embed_query(self, query: str) -> np.ndarray:
        """
        Generate embedding for a search query.
        
        Args:
            query: Search query string
            
        Returns:
            Query embedding vector
        """
        return self.embed(query)[0]
    
    def embed_documents(self, documents: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of documents.
        
        Args:
            documents: List of document texts
            
        Returns:
            Document embeddings matrix
        """
        return self.embed(documents)
    
    @property
    def dimension(self) -> int:
        """Get the embedding dimension."""
        return self.model.get_sentence_embedding_dimension()
