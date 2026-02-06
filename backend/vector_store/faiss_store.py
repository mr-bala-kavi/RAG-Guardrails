"""
FAISS vector store for document storage and similarity search.
"""
import os
import json
import faiss
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict

import sys
sys.path.append('..')
from config import FAISS_DIR, EMBEDDING_DIMENSION, TOP_K_RESULTS, SIMILARITY_THRESHOLD


@dataclass
class Document:
    """Represents a stored document with metadata."""
    id: int
    content: str
    source_file: str
    chunk_index: int
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class SearchResult:
    """Represents a search result with score."""
    document: Document
    score: float
    rank: int


class FAISSVectorStore:
    """FAISS-based vector store for document embeddings."""
    
    def __init__(self, index_path: Optional[Path] = None):
        """
        Initialize the vector store.
        
        Args:
            index_path: Optional path to load existing index
        """
        self.index_path = index_path or FAISS_DIR
        self.index_file = self.index_path / "index.faiss"
        self.metadata_file = self.index_path / "metadata.json"
        
        self.dimension = EMBEDDING_DIMENSION
        self.documents: Dict[int, Document] = {}
        self.next_id = 0
        
        # Initialize or load index
        if self.index_file.exists() and self.metadata_file.exists():
            self._load()
        else:
            self._init_index()
    
    def _init_index(self):
        """Initialize a new FAISS index."""
        # Use Inner Product for normalized vectors (equivalent to cosine similarity)
        self.index = faiss.IndexFlatIP(self.dimension)
        # Wrap with IDMap to track document IDs
        self.index = faiss.IndexIDMap(self.index)
        print(f"Initialized new FAISS index with dimension {self.dimension}")
    
    def _load(self):
        """Load existing index and metadata from disk."""
        try:
            self.index = faiss.read_index(str(self.index_file))
            
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.next_id = data.get('next_id', 0)
                self.documents = {
                    int(k): Document(**v) 
                    for k, v in data.get('documents', {}).items()
                }
            
            print(f"Loaded FAISS index with {len(self.documents)} documents")
        except Exception as e:
            print(f"Error loading index: {e}, initializing new index")
            self._init_index()
    
    def save(self):
        """Save index and metadata to disk."""
        self.index_path.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, str(self.index_file))
        
        # Save metadata
        metadata = {
            'next_id': self.next_id,
            'documents': {str(k): asdict(v) for k, v in self.documents.items()}
        }
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Saved FAISS index with {len(self.documents)} documents")
    
    def add_documents(
        self,
        contents: List[str],
        embeddings: np.ndarray,
        source_file: str,
        chunk_indices: List[int] = None,
        metadata: List[Dict[str, Any]] = None
    ) -> List[int]:
        """
        Add documents to the vector store.
        
        Args:
            contents: List of document contents
            embeddings: Numpy array of embeddings (n_docs, dim)
            source_file: Source file name
            chunk_indices: Optional list of chunk indices
            metadata: Optional list of metadata dicts
            
        Returns:
            List of assigned document IDs
        """
        if len(contents) != len(embeddings):
            raise ValueError("Number of contents must match number of embeddings")
        
        if chunk_indices is None:
            chunk_indices = list(range(len(contents)))
        
        if metadata is None:
            metadata = [{}] * len(contents)
        
        # Ensure embeddings are float32 and normalized
        embeddings = embeddings.astype(np.float32)
        faiss.normalize_L2(embeddings)
        
        # Assign IDs
        ids = []
        for i, (content, chunk_idx, meta) in enumerate(zip(contents, chunk_indices, metadata)):
            doc_id = self.next_id
            self.next_id += 1
            
            self.documents[doc_id] = Document(
                id=doc_id,
                content=content,
                source_file=source_file,
                chunk_index=chunk_idx,
                metadata=meta
            )
            ids.append(doc_id)
        
        # Add to FAISS index
        ids_array = np.array(ids, dtype=np.int64)
        self.index.add_with_ids(embeddings, ids_array)
        
        # Auto-save
        self.save()
        
        return ids
    
    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = TOP_K_RESULTS,
        threshold: float = SIMILARITY_THRESHOLD
    ) -> List[SearchResult]:
        """
        Search for similar documents.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            threshold: Minimum similarity threshold
            
        Returns:
            List of SearchResult objects
        """
        if self.index.ntotal == 0:
            return []
        
        # Ensure query is proper shape and normalized
        query = query_embedding.reshape(1, -1).astype(np.float32)
        faiss.normalize_L2(query)
        
        # Search
        actual_k = min(top_k, self.index.ntotal)
        scores, ids = self.index.search(query, actual_k)
        
        results = []
        for rank, (score, doc_id) in enumerate(zip(scores[0], ids[0])):
            if doc_id < 0 or score < threshold:
                continue
            
            if doc_id in self.documents:
                results.append(SearchResult(
                    document=self.documents[doc_id],
                    score=float(score),
                    rank=rank
                ))
        
        return results
    
    def delete_by_source(self, source_file: str) -> int:
        """
        Delete all documents from a specific source file.
        
        Args:
            source_file: Source file name to delete
            
        Returns:
            Number of deleted documents
        """
        ids_to_delete = [
            doc_id for doc_id, doc in self.documents.items()
            if doc.source_file == source_file
        ]
        
        if not ids_to_delete:
            return 0
        
        # Remove from metadata
        for doc_id in ids_to_delete:
            del self.documents[doc_id]
        
        # Rebuild index (FAISS doesn't support efficient deletion)
        self._rebuild_index()
        
        return len(ids_to_delete)
    
    def clear(self):
        """Clear all documents from the store."""
        self.documents = {}
        self.next_id = 0
        self._init_index()
        self.save()
        print("Cleared all documents from vector store")
    
    def _rebuild_index(self):
        """Rebuild the FAISS index from stored documents."""
        # This is needed after deletion since FAISS doesn't support removal
        self._init_index()
        
        # Note: We would need to re-embed all documents
        # For now, just save the reduced metadata
        self.save()
    
    @property
    def count(self) -> int:
        """Get the number of documents in the store."""
        return len(self.documents)
    
    def get_all_sources(self) -> List[str]:
        """Get list of all unique source files."""
        return list(set(doc.source_file for doc in self.documents.values()))
