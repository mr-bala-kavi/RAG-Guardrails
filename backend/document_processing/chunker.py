"""
Text chunker for splitting documents into overlapping chunks.
"""
from typing import List
from dataclasses import dataclass

import sys
sys.path.append('..')
from config import CHUNK_SIZE, CHUNK_OVERLAP


@dataclass
class TextChunk:
    """Represents a chunk of text with metadata."""
    content: str
    start_index: int
    end_index: int
    chunk_index: int
    source_file: str = ""


class TextChunker:
    """Split text documents into overlapping chunks."""
    
    def __init__(
        self,
        chunk_size: int = CHUNK_SIZE,
        chunk_overlap: int = CHUNK_OVERLAP
    ):
        """
        Initialize the chunker.
        
        Args:
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Number of overlapping characters between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk(self, text: str, source_file: str = "") -> List[TextChunk]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: The text to split
            source_file: Optional source file name for metadata
            
        Returns:
            List of TextChunk objects
        """
        if not text.strip():
            return []
        
        chunks = []
        start = 0
        chunk_index = 0
        
        while start < len(text):
            # Calculate end position
            end = start + self.chunk_size
            
            # If not at the end, try to break at a natural boundary
            if end < len(text):
                # Look for paragraph break
                paragraph_break = text.rfind('\n\n', start, end)
                if paragraph_break > start + self.chunk_size // 2:
                    end = paragraph_break + 2
                else:
                    # Look for sentence break
                    for sep in ['. ', '! ', '? ', '\n']:
                        sentence_break = text.rfind(sep, start, end)
                        if sentence_break > start + self.chunk_size // 2:
                            end = sentence_break + len(sep)
                            break
            
            # Extract chunk
            chunk_text = text[start:end].strip()
            
            if chunk_text:
                chunks.append(TextChunk(
                    content=chunk_text,
                    start_index=start,
                    end_index=end,
                    chunk_index=chunk_index,
                    source_file=source_file
                ))
                chunk_index += 1
            
            # Move start position with overlap
            start = end - self.chunk_overlap
            
            # Ensure we make progress
            if start <= chunks[-1].start_index if chunks else start < 0:
                start = end
        
        return chunks
    
    def chunk_with_context(
        self,
        text: str,
        source_file: str = ""
    ) -> List[TextChunk]:
        """
        Split text into chunks with additional context from adjacent chunks.
        
        Args:
            text: The text to split
            source_file: Optional source file name
            
        Returns:
            List of TextChunk objects with expanded context
        """
        base_chunks = self.chunk(text, source_file)
        
        # Add context from adjacent chunks
        enhanced_chunks = []
        for i, chunk in enumerate(base_chunks):
            context_parts = []
            
            # Add preview from previous chunk
            if i > 0:
                prev_content = base_chunks[i-1].content
                context_parts.append(f"[Previous: ...{prev_content[-100:]}]")
            
            context_parts.append(chunk.content)
            
            # Add preview from next chunk
            if i < len(base_chunks) - 1:
                next_content = base_chunks[i+1].content
                context_parts.append(f"[Next: {next_content[:100]}...]")
            
            enhanced_chunks.append(TextChunk(
                content="\n".join(context_parts),
                start_index=chunk.start_index,
                end_index=chunk.end_index,
                chunk_index=chunk.chunk_index,
                source_file=source_file
            ))
        
        return enhanced_chunks
