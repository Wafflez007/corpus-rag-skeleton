# Project Structure

## Directory Organization

```
/
├── skeleton_core/          # Reusable RAG core logic
│   ├── __init__.py
│   ├── app.py             # Flask application factory
│   ├── vector_store.py    # Vector DB operations (ingest, search)
│   ├── templates/         # Jinja2 templates
│   │   └── index.html
│   └── static/            # CSS and JavaScript
│       ├── styles.css
│       └── app.js
├── app_legal/             # "Legal Eagle" configuration
│   ├── config.py          # Legal mode settings
│   ├── main.py            # Entry point (port 5000)
│   └── __init__.py
├── app_ghost/             # "Ghost/Ouija Board" configuration
│   ├── config.py          # Ghost mode settings
│   ├── main.py            # Entry point (port 5001)
│   └── __init__.py
├── chroma_db/             # ChromaDB persistence (auto-created)
├── .env                   # Environment variables (GOOGLE_API_KEY)
├── requirements.txt       # Python dependencies
└── venv/                  # Virtual environment
```

## Architecture Patterns

### Skeleton + Config Pattern

The `skeleton_core` module contains all shared RAG functionality. Individual app folders provide configuration objects that customize behavior.

### Config Object Structure

Each `app_*/config.py` must define a `Config` class with:
- `APP_NAME`: String for branding (e.g., "Legal Eagle ⚖️")
- `THEME_CSS`: CSS class or theme identifier (e.g., "blue-corporate")
- `SYSTEM_PROMPT`: AI personality instructions (multi-line string with rules)

### Entry Point Pattern

Each app has its own `main.py` that:
1. Adds parent directory to `sys.path` for imports
2. Loads `.env` using `python-dotenv`
3. Imports `create_app` from `skeleton_core.app`
4. Imports `Config` from its own `config.py`
5. Calls `create_app(Config)` and runs Flask on a specific port

### Core Responsibilities

- `skeleton_core/app.py`: Flask routes (`/`, `/upload`, `/chat`), app factory with config injection
- `skeleton_core/vector_store.py`: Document chunking, embedding generation (Gemini), vector search (ChromaDB)
- `app_*/main.py`: Application entry points with port configuration
- `app_*/config.py`: Personality and theme configuration

## Key Routes

- `/`: Main page (renders `index.html` with app name and theme)
- `/upload` (POST): Accepts text/PDF files, chunks by page, generates embeddings, stores in ChromaDB
- `/chat` (POST): Handles user queries with RAG context retrieval (top 3 chunks) and Gemini generation

## Document Processing

Files are processed with page awareness:
- PDFs: Each page extracted separately with page number metadata
- Text files: Treated as single page (page 1)
- Chunks stored with metadata: `source`, `page`, `chunk_index`
- Chunk size: 500 characters with 50 character overlap

## Extension Points

New app modes can be added by:
1. Creating `app_name/` folder
2. Adding `config.py` with `Config` class (APP_NAME, THEME_CSS, SYSTEM_PROMPT)
3. Adding `main.py` entry point with unique port
4. Adding `__init__.py` for package structure
