# Project Spec: Project Corpus - RAG Skeleton

## 1. Project Overview
A generic "Retrieval Augmented Generation" (RAG) web application using Python and Flask. 
The application acts as a "Chat Interface" for uploaded documents. Users upload text/PDF files, and they can chat with their content using AI-powered semantic search.

## 2. The Skeleton Architecture (The Core)
The core logic resides in `skeleton_core`. It is fully reusable and framework-agnostic.
- **Backend:** Flask 3.1.0 (Python 3.10+, tested on 3.13.6)
- **Vector Database:** ChromaDB 0.5.20 (local, persisted to `./chroma_db`)
- **AI Integration:** Google Gemini API (generative-ai 0.8.3) for chat completion and embeddings
- **Frontend:** Custom HTML/CSS (no framework) served via Flask Jinja2 templates

## 3. The Config System (Crucial)
Each app mode loads a configuration class that determines its **Personality** and **RAG Parameters**.
The `Config` class must contain:
- `APP_NAME`: String for branding (e.g., "Legal Eagle ⚖️" or "Ouija Board 🔮")
- `THEME_CSS`: CSS theme identifier (e.g., "blue-corporate" or "dark-gothic")
- `SYSTEM_PROMPT`: The persona instructions sent to the AI (multi-line string with rules)
- `CHUNK_SIZE`: Characters per chunk (default: 500)
- `CHUNK_OVERLAP`: Overlapping characters between chunks (default: 50)
- `TOP_K_RESULTS`: Number of context chunks to retrieve (default: 3)
- `RELEVANCE_THRESHOLD`: Distance threshold for filtering results (default: 0.3)

## 4. Implemented Features
1. **Document Upload (`/upload`):** 
   - Accepts `.txt` or `.pdf` files
   - Extracts text with page awareness (PDFs by page, text as single page)
   - Chunks text with configurable size and overlap
   - Generates embeddings using Gemini `text-embedding-004` model
   - Stores in ChromaDB with metadata (source, page, chunk_index)
   - Real-time progress tracking via Server-Sent Events (SSE)

2. **Chat Interface (`/chat`):**
   - Takes user queries
   - Searches vector DB for semantically relevant context (top K results)
   - Filters results by relevance threshold
   - Optional source filtering to query specific documents
   - Sends context + system prompt + query to Gemini
   - Robust model selection with automatic fallback (prioritizes flash models)
   - Handles safety filter blocks gracefully

3. **Document Management:**
   - `/documents` (GET): Lists all uploaded documents with page and chunk counts
   - `/documents/<source>` (DELETE): Deletes specific documents and all their chunks

4. **Personality Switching:**
   - **Legal Eagle (port 5000):** Professional legal assistant, formal language, precise citations
   - **Ouija Board (port 5001):** Mystical entity, gothic atmosphere, cryptic responses with emojis

## 5. Architecture Patterns
- **Skeleton + Config Pattern:** Core logic in `skeleton_core`, personality overlays in `app_*` folders
- **App Factory Pattern:** `create_app(Config)` injects configuration into Flask app
- **Page-Aware Chunking:** Documents maintain page metadata for accurate source attribution
- **Task-Specific Embeddings:** Uses `retrieval_document` for ingestion, `retrieval_query` for search
- **Graceful Degradation:** AI model fallback strategy ensures availability

## 6. Extension Points
New app modes can be added by:
1. Creating `app_name/` folder with `__init__.py`
2. Adding `config.py` with `Config` class (all required fields)
3. Adding `main.py` entry point with unique port
4. Optionally customizing RAG parameters for the use case

## 7. Current Status
✅ **Phase 1 Complete:** Backend pipeline (Upload -> Vectorize -> Store)
✅ **Phase 2 Complete:** Chat interface with RAG
✅ **Phase 3 Complete:** Two distinct UI themes (Legal Eagle, Ouija Board)
✅ **Phase 4 Complete:** Document management and progress tracking
✅ **Phase 5 Complete:** Production deployment configuration (Render.com)