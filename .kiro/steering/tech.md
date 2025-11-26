# Technology Stack

## Core Technologies

- **Language:** Python 3.10+
- **Web Framework:** Flask 3.0.0 with Jinja2 templating
- **Vector Database:** ChromaDB 0.5.0 (local, persisted to `./chroma_db`)
- **AI Services:** Google Gemini API (generative AI + embeddings)
- **Frontend:** HTML with custom CSS (no framework)

## Key Dependencies

Dependencies are managed in `requirements.txt`:
- `Flask==3.0.0` - Web server
- `google-generativeai==0.3.0` - Gemini AI integration
- `chromadb==0.5.0` - Vector database
- `PyPDF2==3.0.0` - PDF processing (imported as `pypdf`)
- `python-dotenv==1.0.0` - Environment variable management

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run Legal Eagle app (port 5000)
python app_legal/main.py

# Run Ghost/Ouija app (port 5001)
python app_ghost/main.py
```

## Environment Variables

Required in `.env` file:
- `GOOGLE_API_KEY`: Required for Gemini AI functionality (embeddings + generation)

## Code Style

- Follow PEP 8 conventions
- Use type hints where appropriate (see `skeleton_core/app.py` and `vector_store.py`)
- Keep the core (`skeleton_core`) framework-agnostic and reusable
- Use docstrings for all functions and classes

## AI Model Strategy

The app uses a fallback model selection strategy for Gemini:
1. Prioritizes `gemini-1.5-flash` variants for speed and cost
2. Falls back to `gemini-1.0-pro` or `gemini-pro` if flash unavailable
3. Handles safety filter blocks gracefully with user-friendly messages
4. Uses `text-embedding-004` model for embeddings with task-specific types
