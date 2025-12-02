# Project Corpus - RAG Skeleton

A polished, production-ready RAG (Retrieval Augmented Generation) web application that lets you chat with uploaded documents. The unique "skeleton + apps" architecture allows multiple AI personalities and themes to share the same core logic.

## ✨ Key Features

### Core Functionality
- 📄 **Multi-format document support** - Upload and chat with text/PDF documents
- 🔍 **Semantic search** - Vector-based retrieval using ChromaDB with Gemini embeddings
- 🎯 **Smart source attribution** - Relevance-filtered citations showing only documents that actually contain answers
- 📑 **Page-aware chunking** - Track exact page numbers for precise source references
- 📚 **Document library** - Manage multiple documents with selective filtering

### User Experience
- 🎭 **Multiple AI personalities** - Legal Eagle (professional), Ouija Board (mystical), and extensible
- 🎨 **Theme-based UI** - Fully customized styling per personality with smooth animations
- ⚡ **Real-time progress tracking** - SSE-based upload progress with stage indicators
- 📤 **Sequential upload queue** - Handles multiple file uploads gracefully
- ✅ **Comprehensive validation** - File type, size, and content validation with user-friendly errors
- 🎵 **Ambient audio** - Theme-appropriate sound effects (Ghost: ambient drone, Legal: typewriter)
- ♿ **Accessibility** - ARIA labels, screen reader support, keyboard navigation

### Developer Experience
- 🏗️ **Modular architecture** - Reusable core with config-based app modes
- 🧪 **Comprehensive test suite** - Property-based testing for UI components
- 🎨 **CSS custom properties** - Theme variables for easy customization
- 📱 **Responsive design** - Mobile-friendly with adaptive layouts

## 🎭 Available Personalities

### Legal Eagle ⚖️ (Port 5000)
Professional legal document analysis with formal, precise responses.
- **Theme**: Blue corporate styling with legal icons
- **Personality**: Formal, analytical, citation-focused
- **Audio**: Typewriter sound effects
- **Use case**: Legal research, contract analysis, professional documentation

### Ghost/Ouija Board 👻 (Port 5001)
Mystical, spooky interactions with your documents from beyond the veil.
- **Theme**: Dark gothic with blood drip animations
- **Personality**: Cryptic, mystical, dramatic
- **Audio**: Ambient drone with static glitch effects
- **Use case**: Creative writing, atmospheric document exploration

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

## 🚀 Usage

### Running the Application

Start either personality mode:

```bash
# Legal Eagle (port 5000)
python app_legal/main.py

# Ghost/Ouija Board (port 5001)
python app_ghost/main.py
```

Then open your browser to `http://localhost:5000` or `http://localhost:5001`

### Using the Interface

1. **Upload Documents**
   - Click "Choose File" and select a `.txt` or `.pdf` file (max 10MB)
   - Click "UPLOAD" to process the document
   - Watch real-time progress as pages are parsed and vectorized
   - Multiple files can be queued for sequential processing

2. **Manage Document Library**
   - View all uploaded documents in the left sidebar
   - Select/deselect documents to filter which ones are searched
   - Use "Select All" checkbox for quick selection
   - Delete documents with the trash icon

3. **Chat with Documents**
   - Type your question in the chat input
   - Press Enter or click "SEND" to submit
   - AI responds with context from selected documents
   - Source citations show which documents and pages were referenced
   - Only documents containing relevant information are cited

4. **Audio Controls**
   - Click the speaker icon (bottom-right) to toggle sound
   - Ghost mode: ambient background drone + response effects
   - Legal mode: typewriter sound on AI responses

## Architecture

```
skeleton_core/       # Reusable RAG core
├── app.py          # Flask routes and app factory
├── vector_store.py # ChromaDB operations (ingest, search, delete)
├── templates/      # Jinja2 templates
│   └── index.html  # Main chat interface
└── static/         # Frontend assets
    ├── styles.css  # Theme-aware CSS
    ├── app.js      # Client-side JavaScript
    ├── favicon-legal.svg
    ├── favicon-ghost.svg
    └── sounds/     # Audio assets

app_legal/          # Legal Eagle configuration
├── config.py       # Legal mode settings
├── main.py         # Entry point (port 5000)
└── __init__.py

app_ghost/          # Ghost/Ouija configuration
├── config.py       # Ghost mode settings
├── main.py         # Entry point (port 5001)
└── __init__.py

tests/              # Comprehensive test suite
.kiro/              # Kiro IDE configuration
├── steering/       # Project documentation
│   ├── tech.md
│   ├── structure.md
│   ├── product.md
│   └── personalities.md
├── hooks/          # Automated workflows
└── spec.md         # Project specification

launcher.py         # Multi-app launcher for deployment
Procfile            # Render.com deployment config
render.yaml         # Render service configuration
```

### Smart Source Attribution

The system uses relevance-based filtering to ensure accurate source citations:
- Vector search retrieves the top 3 most relevant document chunks
- Results are filtered by similarity threshold (within 0.3 distance units of best match)
- Only documents that actually contain relevant information are shown in citations
- Each citation includes the specific page numbers where information was found

### Document Processing Pipeline

1. **File Upload** → SSE progress streaming with stage updates
2. **Page Extraction** → PDF pages or text file parsed individually
3. **Chunking** → 500 character chunks with 50 character overlap
4. **Embedding** → Gemini `text-embedding-004` with task-specific types
5. **Storage** → ChromaDB with metadata (source, page, chunk_index)

### Chat Query Flow

1. **User Query** → Optional document filtering via library selection
2. **Vector Search** → Semantic similarity search in ChromaDB
3. **Relevance Filter** → Distance-based threshold filtering
4. **Context Assembly** → Top chunks combined for AI prompt
5. **AI Generation** → Gemini Flash with personality-specific system prompt
6. **Response Display** → Typewriter effect with source citations

## 🛠️ Creating New Personalities

The skeleton architecture makes it easy to add new AI personalities:

1. **Create app folder**: `app_yourname/`
2. **Add `config.py`**:
   ```python
   class Config:
       # Branding
       APP_NAME = "Your App Name 🎯"
       THEME_CSS = "your-theme-class"
       
       # RAG Configuration (optional - uses defaults if omitted)
       CHUNK_SIZE = 500              # Characters per chunk
       CHUNK_OVERLAP = 50            # Overlap between chunks
       TOP_K_RESULTS = 3             # Number of results to retrieve
       RELEVANCE_THRESHOLD = 0.3     # Distance threshold for filtering
       
       # AI Personality
       SYSTEM_PROMPT = """
       Your personality instructions here.
       Define tone, style, and behavior.
       """
   ```
3. **Add `main.py`**:
   ```python
   import sys
   import os
   sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
   
   from dotenv import load_dotenv
   load_dotenv()
   
   from skeleton_core.app import create_app
   from .config import Config
   
   if __name__ == '__main__':
       app = create_app(Config)
       app.run(debug=True, port=5002)  # Use unique port
   ```
4. **Add `__init__.py`** (empty file for package structure)
5. **Customize CSS** in `skeleton_core/static/styles.css`:
   ```css
   .theme-your-theme-class {
       --primary: #your-color;
       --accent: #your-accent;
       /* ... other variables */
   }
   ```
6. **Optional**: Add custom audio files to `skeleton_core/static/sounds/`

## 🧪 Testing

The project includes comprehensive property-based tests using Hypothesis:

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_animations.py

# Run with verbose output
pytest -v tests/
```

**Test Coverage:**
- UI animations and transitions
- Auto-scroll behavior
- CSS property validation
- Enter key submission
- Error display and handling
- File validation (type, size, content)
- Loading indicators
- Message display and formatting
- Sequential upload queue
- Upload progress tracking
- Success/error feedback

## 📚 Tech Stack

**Backend:**
- Python 3.10+ (tested on 3.13.6)
- Flask 3.1.0 - Web framework with Jinja2 templating
- ChromaDB 0.5.20 - Vector database with cosine similarity
- Google Gemini API 0.8.3 - AI generation (`gemini-1.5-flash`) and embeddings (`text-embedding-004`)
- pypdf 5.1.0 - PDF text extraction
- python-dotenv 1.0.1 - Environment variable management

**Frontend:**
- Vanilla JavaScript - No framework dependencies
- Custom CSS - Theme-based styling with CSS variables
- CSS Custom Properties - Theme variables for easy customization
- Server-Sent Events (SSE) - Real-time upload progress
- Web Audio API - Sound effects

**Testing:**
- pytest 7.4.3 - Test framework
- Hypothesis 6.92.1 - Property-based testing

## 🎯 Project Highlights

- **Production-ready UI** with polished animations, error handling, and accessibility
- **Robust upload system** with validation, progress tracking, and queue management
- **Smart RAG pipeline** with relevance filtering and accurate source attribution
- **Extensible architecture** - add new personalities without touching core code
- **Comprehensive testing** - property-based tests ensure UI reliability
- **Theme system** - CSS variables enable complete visual customization
- **Audio integration** - personality-specific sound design
- **Kiro IDE hooks** - Automated validation and testing on file save
- **Deployment ready** - Configured for Render.com with Procfile and launcher script

## 📝 License

MIT

## 🚢 Deployment

The project is configured for deployment on Render.com:

1. **Environment Variables**: Set `GOOGLE_API_KEY` in Render dashboard
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `python launcher.py` (runs both apps on dynamic ports)

The `launcher.py` script automatically detects the PORT environment variable and runs the appropriate app mode.

## 🎮 Kiro IDE Hooks

The project includes automated workflows for development:

- **config-validator** - Validates config.py files have all required fields
- **env-check-on-session** - Verifies GOOGLE_API_KEY on session start
- **test-runner-on-save** - Runs pytest automatically when Python files are saved
- **update-steering-on-config-change** - Reminds to update documentation when configs change
- **vector-store-health-check** - Runs diagnostics on vector_store.py changes

## 🤝 Contributing

Contributions welcome! Areas for expansion:
- New personality modes (Detective, Scientist, Poet, etc.)
- Additional document formats (DOCX, Markdown, HTML)
- Advanced RAG features (multi-query, re-ranking, citations in text)
- UI enhancements (dark mode toggle, custom themes, mobile gestures)
- Additional deployment targets (Docker, AWS, Azure)
