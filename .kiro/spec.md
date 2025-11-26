# Project Spec: The "Medium" RAG Skeleton

## 1. Project Overview
We are building a generic "Retrieval Augmented Generation" (RAG) web application using Python and Flask. 
The application acts as a "Chat Interface" for uploaded documents. Users upload a text/PDF, and they can chat with it.

## 2. The Skeleton Architecture (The Core)
The core logic resides in `skeleton_core`. It must be reusable.
- **Backend:** Flask (Python 3.10+)
- **Database:** PostgreSQL (using `pgvector` extension) OR `ChromaDB` (local) for storing vector embeddings.
- **AI Integration:** OpenAI API (ChatCompletion + Embeddings).
- **Frontend:** Simple HTML/TailwindCSS (served via Flask Jinja2).

## 3. The Config System (Crucial)
The app must load a configuration file that determines its **Personality**.
The `Config` object must contain:
- `APP_NAME`: String (e.g., "Legal Eagle" or "Ouija Board")
- `THEME_CSS`: String (e.g., "blue-corporate" or "dark-gothic")
- `SYSTEM_PROMPT`: The 'persona' instructions sent to the AI.

## 4. Required Features
1.  **Ingest:** A route `/upload` that accepts `.txt` or `.pdf`, extracts text, chunks it, and saves embeddings.
2.  **Chat:** A route `/chat` that takes user input, searches the vector DB for context, and sends the context + prompt to OpenAI.
3.  **Switching Logic:** - If `APP_MODE` is "LEGAL", the System Prompt must be: "You are a precise, professional lawyer. Cite your sources."
    - If `APP_MODE` is "OUIJA", the System Prompt must be: "You are a spirit trapped in this document. Speak in riddles. Use spooky emojis."

## 5. Development Phases
1.  **Phase 1:** Build the backend pipeline (Upload -> Vectorize -> Store).
2.  **Phase 2:** Build the Chat interface.
3.  **Phase 3:** Create the two distinct UI themes (CSS).