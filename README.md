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
- 🎨 **Modern UI with Tailwind CSS + DaisyUI** - Utility-first styling with pre-built components and custom themes
- ⚡ **Real-time progress tracking** - SSE-based upload progress with stage indicators
- 📤 **Sequential upload queue** - Handles multiple file uploads gracefully
- ✅ **Comprehensive validation** - File type, size, and content validation with user-friendly errors
- 🎵 **Ambient audio** - Theme-appropriate sound effects (Ghost: ambient drone, Legal: typewriter)
- ♿ **Accessibility** - ARIA labels, screen reader support, keyboard navigation, WCAG AA compliant
- 📱 **Fully responsive** - Mobile-first design with Tailwind breakpoints

### Developer Experience
- 🏗️ **Modular architecture** - Reusable core with config-based app modes
- 🧪 **Comprehensive test suite** - Property-based testing for UI components
- 🎨 **Tailwind CSS + DaisyUI** - Utility-first styling with themeable components
- 📱 **Responsive design** - Mobile-first with Tailwind breakpoints (sm, md, lg, xl)
- 🔧 **CDN-based setup** - No build tools required, instant development

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

### Directory Structure

```
skeleton_core/       # Reusable RAG core
├── app.py          # Flask routes and app factory
├── vector_store.py # ChromaDB operations (ingest, search, delete)
├── templates/      # Jinja2 templates
│   └── index.html  # Main chat interface (Tailwind + DaisyUI)
└── static/         # Frontend assets
    ├── styles.css  # Minimal custom CSS (~500 lines)
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
├── specs/          # Feature specifications
│   └── tailwind-daisyui-integration/
│       ├── requirements.md
│       ├── design.md
│       ├── tasks.md
│       ├── MIGRATION_GUIDE.md
│       └── COMPONENT_PATTERNS.md
├── hooks/          # Automated workflows
└── spec.md         # Project specification

launcher.py         # Multi-app launcher for deployment
Procfile            # Render.com deployment config
render.yaml         # Render service configuration
```

### UI Stack

```
┌─────────────────────────────────────────────────────────┐
│                    HTML Templates                        │
│  (index.html with Jinja2 templating)                    │
└────────────────┬────────────────────────────────────────┘
                 │
                 ├─► Tailwind CSS 3.x (CDN)
                 │   └─► Utility classes for layout, spacing, colors
                 │
                 ├─► DaisyUI 4.4.19 (CDN)
                 │   └─► Pre-built components (buttons, cards, inputs)
                 │
                 └─► Custom CSS (~500 lines)
                     └─► Theme-specific effects (animations, cursors)
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

## 🎨 Tailwind CSS + DaisyUI Integration

The project uses **Tailwind CSS** (utility-first framework) and **DaisyUI** (component library) for modern, maintainable styling.

### Why Tailwind + DaisyUI?

- **Utility-first approach** - Build custom designs without writing CSS
- **Pre-built components** - DaisyUI provides buttons, cards, inputs, chat bubbles, etc.
- **Theme system** - Easy color customization per app personality
- **Responsive by default** - Mobile-first with intuitive breakpoints
- **No build tools** - CDN-based for instant development
- **Minimal custom CSS** - Only ~500 lines for unique effects (vs. 1800+ before)

### Setup

Both Tailwind CSS and DaisyUI are loaded via CDN in `skeleton_core/templates/index.html`:

```html
<!-- Tailwind CSS -->
<script src="https://cdn.tailwindcss.com"></script>

<!-- DaisyUI -->
<link href="https://cdn.jsdelivr.net/npm/daisyui@4.4.19/dist/full.min.css" rel="stylesheet" />
```

### Theme Configuration

Each app mode has a custom DaisyUI theme defined inline:

**Legal Eagle Theme** (Professional Blue):
```javascript
tailwind.config = {
  daisyui: {
    themes: [{
      "legal-eagle": {
        "primary": "#0f172a",      // Deep slate navy
        "secondary": "#334155",    // Steel grey
        "accent": "#ca8a04",       // Muted gold
        "base-100": "#f8fafc",     // Light background
        // ... more colors
      }
    }]
  }
}
```

**Ouija Board Theme** (Dark Gothic):
```javascript
tailwind.config = {
  daisyui: {
    themes: [{
      "ouija-board": {
        "primary": "#8b0000",      // Deep blood red
        "accent": "#ff3f3f",       // Bright red glow
        "base-100": "#050505",     // Void black
        // ... more colors
      }
    }]
  }
}
```

### Common Component Patterns

**Buttons:**
```html
<!-- Primary button -->
<button class="btn btn-primary">UPLOAD</button>

<!-- Accent button with icon -->
<button class="btn btn-accent">
  <span>🔮</span> Summon Spirits
</button>

<!-- Minimum touch target size (44x44px) -->
<button class="btn btn-primary min-h-[44px] min-w-[44px]">SEND</button>
```

**Cards:**
```html
<div class="card bg-base-200 shadow-xl">
  <div class="card-body">
    <h2 class="card-title">📂 Upload Documents</h2>
    <p>Card content goes here</p>
  </div>
</div>
```

**Inputs:**
```html
<!-- Text input -->
<input type="text" class="input input-bordered w-full" placeholder="Enter query..." />

<!-- File input -->
<input type="file" class="file-input file-input-bordered" />

<!-- Textarea -->
<textarea class="textarea textarea-bordered" rows="4"></textarea>
```

**Chat Bubbles:**
```html
<!-- User message (right side) -->
<div class="chat chat-end">
  <div class="chat-bubble chat-bubble-primary">User message</div>
</div>

<!-- AI message (left side) -->
<div class="chat chat-start">
  <div class="chat-bubble">AI response</div>
</div>
```

**Progress Bars:**
```html
<progress class="progress progress-primary" value="70" max="100"></progress>
```

**Alerts:**
```html
<div class="alert alert-error">
  <span>⚠️ Error message here</span>
</div>

<div class="alert alert-success">
  <span>✅ Success message here</span>
</div>
```

**Loading Indicators:**
```html
<span class="loading loading-spinner loading-lg"></span>
```

### Responsive Design

Tailwind uses mobile-first breakpoints:

```html
<!-- Stack on mobile, side-by-side on desktop -->
<div class="flex flex-col lg:flex-row gap-4">
  <div class="flex-1">Left column</div>
  <div class="flex-1">Right column</div>
</div>

<!-- 1 column on mobile, 3 columns on desktop -->
<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
  <div>Column 1</div>
  <div>Column 2</div>
  <div>Column 3</div>
</div>
```

**Breakpoints:**
- `sm:` - 640px and up (small tablets)
- `md:` - 768px and up (tablets)
- `lg:` - 1024px and up (desktops)
- `xl:` - 1280px and up (large desktops)

### Custom Effects Preserved

Some unique visual effects remain in custom CSS (`skeleton_core/static/styles.css`):

**Ouija Board Effects:**
- Blood drip animations (`.blood-drip`)
- Mystical fog overlay (`.mystical-fog`)
- Planchette cursor (`.planchette-cursor`)
- Title pulse animation (`.title-pulse`)

These effects cannot be replicated with Tailwind utilities and are preserved for the mystical aesthetic.

### Accessibility

All components meet WCAG AA standards:
- **Color contrast**: 14.5:1 (Legal Eagle), 18.2:1 (Ouija Board)
- **Touch targets**: Minimum 44x44px on all interactive elements
- **Focus indicators**: Visible focus rings on all buttons/inputs
- **Keyboard navigation**: Full keyboard support with proper tab order
- **Screen readers**: ARIA labels and semantic HTML

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
5. **Configure DaisyUI theme** in your template's inline config:
   ```javascript
   tailwind.config = {
     daisyui: {
       themes: [{
         "your-theme-name": {
           "primary": "#your-color",
           "secondary": "#your-secondary",
           "accent": "#your-accent",
           "base-100": "#background-color",
           // ... see DaisyUI docs for all options
         }
       }]
     }
   }
   ```
6. **Apply theme** by setting `data-theme="your-theme-name"` on the `<html>` tag
7. **Optional**: Add custom CSS effects in `skeleton_core/static/styles.css` for unique animations
8. **Optional**: Add custom audio files to `skeleton_core/static/sounds/`

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
- **Tailwind CSS 3.x** - Utility-first CSS framework (CDN)
- **DaisyUI 4.4.19** - Component library built on Tailwind (CDN)
- Custom CSS - Minimal theme-specific effects (blood drips, mystical fog)
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

## 📖 Documentation

### Project Documentation

- **README.md** - This file, project overview and setup
- **LICENSE** - MIT license

### Steering Documents (`.kiro/steering/`)

- **tech.md** - Technology stack and dependencies
- **structure.md** - Project structure and architecture patterns
- **product.md** - Product overview and capabilities
- **personalities.md** - AI personality configurations

### Tailwind/DaisyUI Documentation (`.kiro/specs/tailwind-daisyui-integration/`)

- **requirements.md** - Requirements for Tailwind/DaisyUI integration
- **design.md** - Design document with architecture and correctness properties
- **tasks.md** - Implementation task list
- **MIGRATION_GUIDE.md** - Comprehensive migration guide from custom CSS
- **COMPONENT_PATTERNS.md** - Quick reference for common UI patterns

### Quick Links

- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [DaisyUI Components](https://daisyui.com/components/)
- [DaisyUI Themes](https://daisyui.com/docs/themes/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Google Gemini API](https://ai.google.dev/docs)

## 🤝 Contributing

Contributions welcome! Areas for expansion:
- New personality modes (Detective, Scientist, Poet, etc.)
- Additional document formats (DOCX, Markdown, HTML)
- Advanced RAG features (multi-query, re-ranking, citations in text)
- UI enhancements (dark mode toggle, custom themes, mobile gestures)
- Additional deployment targets (Docker, AWS, Azure)

### Development Workflow

1. **Read the documentation** - Start with steering files and migration guide
2. **Follow component patterns** - Use established patterns from COMPONENT_PATTERNS.md
3. **Test your changes** - Run pytest suite before committing
4. **Maintain accessibility** - Ensure WCAG AA compliance
5. **Update documentation** - Keep docs in sync with code changes
