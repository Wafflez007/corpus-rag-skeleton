"""Vector store operations using ChromaDB"""

import os
import logging
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
import google.generativeai as genai

logger = logging.getLogger(__name__)


class VectorStore:
    """Handles document chunking, embedding, and retrieval using ChromaDB"""
    
    def __init__(self, collection_name: str = "documents", chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Initialize ChromaDB client and collection.
        
        Args:
            collection_name: Name of the ChromaDB collection
            chunk_size: Maximum characters per chunk
            chunk_overlap: Number of overlapping characters between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        self.client = chromadb.Client(Settings(
            persist_directory="./chroma_db",
            anonymized_telemetry=False
        ))
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        # Configure Google Gemini
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    
    def chunk_text(self, text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Input text to chunk
            chunk_size: Maximum characters per chunk (uses instance default if None)
            overlap: Number of overlapping characters between chunks (uses instance default if None)
            
        Returns:
            List of text chunks
        """
        # Use instance defaults if not specified
        chunk_size = chunk_size or self.chunk_size
        overlap = overlap or self.chunk_overlap
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk.strip())
            start += chunk_size - overlap
        
        return chunks
    
    def get_embedding(self, text: str) -> List[float]:
        """
        Generate embedding using Google Gemini API.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    
    def ingest_document(self, file_data: List[Dict[str, Any]], document_id: str, metadata: Dict[str, Any] = None) -> int:
        """
        Chunk text from specific pages, generate embeddings, and store in ChromaDB.
        
        Args:
            file_data: List of dicts [{'text': '...', 'page': 1}, ...]
            document_id: Unique identifier for the document
            metadata: Base metadata
        """
        ids = []
        embeddings = []
        documents = []
        metadatas = []

        chunk_counter = 0

        logger.info(f"Processing {len(file_data)} pages for document: {document_id}")

        for page_data in file_data:
            page_text = page_data['text']
            page_num = page_data['page']
            
            # Chunk this specific page
            chunks = self.chunk_text(page_text)
            
            for i, chunk in enumerate(chunks):
                if not chunk: continue
                
                embed = self.get_embedding(chunk)
                if embed:
                    chunk_id = f"{document_id}_p{page_num}_{i}"
                    ids.append(chunk_id)
                    embeddings.append(embed)
                    documents.append(chunk)
                    
                    # Store rich metadata including Page Number
                    metadatas.append({
                        **(metadata or {}), 
                        "chunk_index": chunk_counter, 
                        "source": document_id,
                        "page": page_num  # <--- The Key Addition
                    })
                    chunk_counter += 1

        # Batch add to ChromaDB
        if ids:
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )
            logger.info(f"Successfully ingested {len(ids)} chunks from {document_id}")
        else:
            logger.warning(f"No chunks generated for document: {document_id}")
        
        return len(ids)
    
    def search(self, query: str, n_results: int = 3, filter_sources: List[str] = None) -> List[Dict[str, Any]]:
        """
        Search for relevant chunks using semantic similarity.
        
        Args:
            query: Search query
            n_results: Number of results to return
            filter_sources: Optional list of document sources to filter by
            
        Returns:
            List of matching chunks with metadata
        """
        # Use task_type="retrieval_query" for search queries
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=query,
            task_type="retrieval_query"
        )
        query_embedding = result['embedding']
        
        # Build where filter if sources specified
        where_filter = None
        if filter_sources:
            where_filter = {"source": {"$in": filter_sources}}
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_filter
        )
        
        # Format results
        matches = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                matches.append({
                    'text': doc,
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'distance': results['distances'][0][i] if results['distances'] else None
                })
        
        return matches
    
    def list_documents(self) -> List[Dict[str, Any]]:
        """
        List all unique documents in the collection.
        
        Returns:
            List of documents with metadata (source, page count, chunk count)
        """
        # Get all items from collection
        all_items = self.collection.get()
        
        if not all_items['metadatas']:
            return []
        
        # Group by source
        docs = {}
        for metadata in all_items['metadatas']:
            source = metadata.get('source', 'unknown')
            if source not in docs:
                docs[source] = {
                    'source': source,
                    'pages': set(),
                    'chunks': 0
                }
            docs[source]['pages'].add(metadata.get('page', 1))
            docs[source]['chunks'] += 1
        
        # Convert to list format
        result = []
        for doc in docs.values():
            result.append({
                'source': doc['source'],
                'pages': len(doc['pages']),
                'chunks': doc['chunks']
            })
        
        return sorted(result, key=lambda x: x['source'])
    
    def delete_document(self, source: str) -> int:
        """
        Delete all chunks for a specific document.
        
        Args:
            source: Document source identifier
            
        Returns:
            Number of chunks deleted
        """
        # Get all IDs for this source
        results = self.collection.get(
            where={"source": source}
        )
        
        if results['ids']:
            self.collection.delete(ids=results['ids'])
            return len(results['ids'])
        
        return 0
