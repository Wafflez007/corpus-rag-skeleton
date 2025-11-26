# Project Corpus - RAG Skeleton

A configurable RAG (Retrieval Augmented Generation) web application that lets you chat with uploaded documents. The unique "skeleton + apps" architecture allows multiple AI personalities and themes to share the same core logic.

## Features

- 📄 Upload and chat with text/PDF documents
- 🔍 Vector-based semantic search using ChromaDB
- 🎭 Multiple AI personalities (Legal Eagle, Ouija Board, and more)
- 🎨 Theme-based UI customization
- 📑 Page-aware document chunking with source tracking
- 🤖 Powered by Google Gemini AI

## Available Apps

### Legal Eagle ⚖️ (Port 5000)
Professional legal document analysis with formal, precise responses.

### Ghost/Ouija Board 👻 (Port 5001)
Mystical, spooky interactions with your documents from beyond the veil.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/corpus-rag-skeleton.git
cd corpus-rag-skeleton
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file with your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

## Usage

Run either app mode:

```bash
# Legal Eagle (port 5000)
python app_legal/main.py

# Ghost/Ouija Board (port 5001)
python app_ghost/main.py
```

Then open your browser to `http://localhost:5000` or `http://localhost:5001`

## Architecture

```
skeleton_core/       # Reusable RAG core
├── app.py          # Flask routes and app factory
├── vector_store.py # ChromaDB operations
├── templates/      # Jinja2 templates
└── static/         # CSS and JavaScript

app_legal/          # Legal Eagle configuration
app_ghost/          # Ghost/Ouija configuration
```

## Creating New App Modes

1. Create a new folder: `app_yourname/`
2. Add `config.py` with `Config` class (APP_NAME, THEME_CSS, SYSTEM_PROMPT)
3. Add `main.py` entry point with unique port
4. Add `__init__.py`

## Tech Stack

- Python 3.10+
- Flask 3.0.0
- ChromaDB 0.5.0
- Google Gemini API
- PyPDF2 for PDF processing

## License

MIT
