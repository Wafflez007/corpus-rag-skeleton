# Project Structure

## Directory Organization

```
/
├── skeleton_core/          # Reusable RAG core logic
│   ├── __init__.py
│   ├── app.py             # Flask application factory
│   ├── vector_store.py    # Vector DB operations (ingest, search, delete)
│   ├── templates/         # Jinja2 templates
│   │   └── index.html     # Main chat interface (with Tailwind + DaisyUI)
│   └── static/            # Frontend assets
│       ├── styles.css     # Minimal custom CSS (~500 lines, theme-specific effects)
│       ├── app.js         # Client-side JavaScript
│       ├── favicon-legal.svg   # Legal Eagle favicon
│       ├── favicon-ghost.svg   # Ouija Board favicon
│       └── sounds/        # Audio assets (if any)
├── app_legal/             # "Legal Eagle" configuration
│   ├── config.py          # Legal mode settings
│   ├── main.py            # Entry point (port 5000)
│   └── __init__.py
├── app_ghost/             # "Ghost/Ouija Board" configuration
│   ├── config.py          # Ghost mode settings
│   ├── main.py            # Entry point (port 5001)
│   └── __init__.py
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── test_animations.py
│   ├── test_auto_scroll.py
│   ├── test_css_properties.py
│   ├── test_document_management.py
│   ├── test_enter_key_submission.py
│   ├── test_error_display.py
│   ├── test_file_validation.py
│   ├── test_loading_indicators.py
│   ├── test_message_display.py
│   ├── test_sequential_upload.py
│   ├── test_upload_error_feedback.py
│   ├── test_upload_progress.py
│   ├── test_upload_success_feedback.py
│   ├── test_tailwind_daisyui_cdn.py
│   ├── test_daisyui_theme_config.py
│   ├── test_theme_switching.py
│   └── ... (more Tailwind/DaisyUI tests)
├── .kiro/                 # Kiro IDE configuration
│   ├── steering/          # Steering documents
│   │   ├── tech.md
│   │   ├── structure.md
│   │   ├── product.md
│   │   └── personalities.md
│   ├── specs/             # Feature specifications
│   │   └── tailwind-daisyui-integration/
│   │       ├── requirements.md
│   │       ├── design.md
│   │       ├── tasks.md
│   │       ├── MIGRATION_GUIDE.md
│   │       └── COMPONENT_PATTERNS.md
│   └── spec.md            # Project specification
├── chroma_db/             # ChromaDB persistence (auto-created)
├── venv/                  # Virtual environment
├── .env                   # Environment variables (GOOGLE_API_KEY)
├── .gitignore             # Git ignore rules
├── launcher.py            # Multi-app launcher script
├── requirements.txt       # Python dependencies
├── runtime.txt            # Python version for deployment
├── Procfile               # Render.com deployment config
├── render.yaml            # Render.com service configuration
├── README.md              # Project documentation
└── LICENSE                # License file
```

## Architecture Patterns

### Skeleton + Config Pattern

The `skeleton_core` module contains all shared RAG functionality. Individual app folders provide configuration objects that customize behavior.

### Config Object Structure

Each `app_*/config.py` must define a `Config` class with:
- `APP_NAME`: String for branding (e.g., "Legal Eagle ⚖️")
- `THEME_CSS`: CSS class or theme identifier (e.g., "blue-corporate")
- `SYSTEM_PROMPT`: AI personality instructions (multi-line string with rules)
- `CHUNK_SIZE`: Characters per chunk (default: 500)
- `CHUNK_OVERLAP`: Overlapping characters between chunks (default: 50)
- `TOP_K_RESULTS`: Number of context chunks to retrieve (default: 3)
- `RELEVANCE_THRESHOLD`: Distance threshold for filtering results (default: 0.3)

### Entry Point Pattern

Each app has its own `main.py` that:
1. Adds parent directory to `sys.path` for imports
2. Loads `.env` using `python-dotenv`
3. Imports `create_app` from `skeleton_core.app`
4. Imports `Config` from its own `config.py`
5. Calls `create_app(Config)` and runs Flask on a specific port

### Core Responsibilities

- `skeleton_core/app.py`: Flask routes (`/`, `/upload`, `/chat`, `/documents`), app factory with config injection, robust model selection with fallback strategy
- `skeleton_core/vector_store.py`: Document chunking, embedding generation (Gemini), vector search (ChromaDB), document management (list/delete)
- `app_*/main.py`: Application entry points with port configuration
- `app_*/config.py`: Personality, theme, and RAG parameter configuration

## Key Routes

- `/`: Main page (renders `index.html` with app name, theme, and active model)
- `/upload` (POST): Accepts text/PDF files, chunks by page, generates embeddings, stores in ChromaDB with SSE progress updates
- `/chat` (POST): Handles user queries with RAG context retrieval and Gemini generation (supports optional source filtering)
- `/documents` (GET): Lists all uploaded documents with page and chunk counts
- `/documents/<source>` (DELETE): Deletes a specific document and all its chunks

## Document Processing

Files are processed with page awareness:
- PDFs: Each page extracted separately with page number metadata
- Text files: Treated as single page (page 1)
- Chunks stored with metadata: `source`, `page`, `chunk_index`
- Chunk size: Configurable per app (default 500 characters with 50 character overlap)
- Upload progress tracked via Server-Sent Events (SSE) with stages: reading, parsing, vectorizing, finalizing
- Embeddings generated using `text-embedding-004` model with task-specific types (`retrieval_document` for ingestion, `retrieval_query` for search)

## Extension Points

New app modes can be added by:
1. Creating `app_name/` folder
2. Adding `config.py` with `Config` class (APP_NAME, THEME_CSS, SYSTEM_PROMPT)
3. Adding `main.py` entry point with unique port
4. Adding `__init__.py` for package structure
5. Configuring DaisyUI theme in template's inline config
6. Applying theme via `data-theme` attribute on `<html>` tag

## UI Architecture (Tailwind + DaisyUI)

### CDN Integration

Both Tailwind CSS and DaisyUI are loaded via CDN in `skeleton_core/templates/index.html`:
- Tailwind CSS 3.x from `cdn.tailwindcss.com`
- DaisyUI 4.4.19 from `cdn.jsdelivr.net`
- No build process required for development

### Theme System

Each app mode defines a custom DaisyUI theme inline:
- Legal Eagle: `legal-eagle` theme (professional blue)
- Ouija Board: `ouija-board` theme (dark gothic)
- Themes applied via `data-theme` attribute on `<html>` tag
- Theme colors: primary, secondary, accent, base-100/200/300, semantic colors

### Component Usage

Standard UI components use DaisyUI classes:
- Buttons: `btn btn-primary`, `btn btn-accent`
- Cards: `card bg-base-200 shadow-xl`
- Inputs: `input input-bordered`, `file-input file-input-bordered`
- Chat: `chat chat-start/chat-end`, `chat-bubble`
- Progress: `progress progress-primary`
- Alerts: `alert alert-error/success/info/warning`
- Loading: `loading loading-spinner`

### Custom CSS

Minimal custom CSS (~500 lines) in `skeleton_core/static/styles.css` for:
- Blood drip animations (Ouija Board)
- Mystical fog effects (Ouija Board)
- Planchette cursor (Ouija Board)
- Title pulse animations (both themes)
- Other unique visual effects that cannot be replicated with Tailwind

### Responsive Design

Mobile-first approach using Tailwind breakpoints:
- Default: Mobile (0px+)
- `sm:` Small tablets (640px+)
- `md:` Tablets (768px+)
- `lg:` Desktops (1024px+)
- `xl:` Large desktops (1280px+)

### Accessibility

All components meet WCAG AA standards:
- Minimum 44x44px touch targets: `min-h-[44px] min-w-[44px]`
- High color contrast ratios (14.5:1 Legal, 18.2:1 Ouija)
- Visible focus indicators (DaisyUI built-in)
- Semantic HTML with ARIA labels
- Keyboard navigation support
