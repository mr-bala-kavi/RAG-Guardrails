"""
Document retriever for fetching relevant chunks from the vector store.
"""
from typing import List, Optional
import numpy as np

import sys
sys.path.append('..')
from vector_store.faiss_store import FAISSVectorStore, SearchResult
from document_processing.embedder import EmbeddingModel
from config import TOP_K_RESULTS, SIMILARITY_THRESHOLD


class DocumentRetriever:
    """Retrieve relevant documents based on query similarity."""
    
    def __init__(
        self,
        vector_store: Optional[FAISSVectorStore] = None,
        embedding_model: Optional[EmbeddingModel] = None
    ):
        """
        Initialize the retriever.
        
        Args:
            vector_store: Vector store instance
            embedding_model: Embedding model instance
        """
        self.vector_store = vector_store or FAISSVectorStore()
        self.embedding_model = embedding_model or EmbeddingModel()
    
    def retrieve(
        self,
        query: str,
        top_k: int = TOP_K_RESULTS,
        threshold: float = SIMILARITY_THRESHOLD
    ) -> List[SearchResult]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: User query string
            top_k: Maximum number of results
            threshold: Minimum similarity threshold
            
        Returns:
            List of SearchResult objects
        """
        # Generate query embedding
        query_embedding = self.embedding_model.embed_query(query)
        
        # Search vector store
        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            threshold=threshold
        )
        
        return results
    
    def retrieve_with_scores(
        self,
        query: str,
        top_k: int = TOP_K_RESULTS
    ) -> List[dict]:
        """
        Retrieve documents with detailed score information.
        
        Args:
            query: User query string
            top_k: Maximum number of results
            
        Returns:
            List of dicts with document info and scores
        """
        results = self.retrieve(query, top_k=top_k, threshold=0.0)
        
        return [
            {
                "content": r.document.content,
                "source": r.document.source_file,
                "chunk_index": r.document.chunk_index,
                "similarity_score": r.score,
                "rank": r.rank
            }
            for r in results
        ]
    
    def format_context(
        self,
        results: List[SearchResult],
        max_length: Optional[int] = None
    ) -> str:
        """
        Format retrieved results into a context string for the LLM.
        
        Args:
            results: List of search results
            max_length: Optional maximum context length
            
        Returns:
            Formatted context string
        """
        if not results:
            return "No relevant documents found."
        
        context_parts = []
        total_length = 0
        
        for i, result in enumerate(results, 1):
            chunk_header = f"[Source: {result.document.source_file}, Chunk {result.document.chunk_index}]"
            chunk_content = result.document.content
            chunk_text = f"{chunk_header}\n{chunk_content}"
            
            # Check length limit
            if max_length and total_length + len(chunk_text) > max_length:
                remaining = max_length - total_length
                if remaining > 100:
                    chunk_text = chunk_text[:remaining] + "..."
                    context_parts.append(chunk_text)
                break
            
            context_parts.append(chunk_text)
            total_length += len(chunk_text) + 2  # +2 for newlines
        
        return "\n\n".join(context_parts)
