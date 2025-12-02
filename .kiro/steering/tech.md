# Technology Stack

## Core Technologies

- **Language:** Python 3.10+ (tested on 3.13.6)
- **Web Framework:** Flask 3.1.0 with Jinja2 templating
- **Vector Database:** ChromaDB 0.5.20 (local, persisted to `./chroma_db`)
- **AI Services:** Google Gemini API (generative AI + embeddings)
- **Frontend:** Tailwind CSS 3.x + DaisyUI 4.4.19 (CDN-based), minimal custom CSS

## Key Dependencies

Dependencies are managed in `requirements.txt`:
- `Flask==3.1.0` - Web server
- `google-generativeai==0.8.3` - Gemini AI integration
- `chromadb==0.5.20` - Vector database
- `pypdf==5.1.0` - PDF processing
- `python-dotenv==1.0.1` - Environment variable management
- `pytest==7.4.3` - Testing framework
- `hypothesis==6.92.1` - Property-based testing

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

## UI Framework

### Tailwind CSS + DaisyUI

The project uses a CDN-based approach for styling:
- **Tailwind CSS 3.x**: Utility-first CSS framework loaded via CDN
- **DaisyUI 4.4.19**: Component library built on Tailwind, also via CDN
- **Custom CSS**: Minimal (~500 lines) for theme-specific effects only

### Theme Configuration

Each app mode defines a custom DaisyUI theme inline in the HTML template:
- Legal Eagle: Professional blue theme (`legal-eagle`)
- Ouija Board: Dark gothic theme (`ouija-board`)
- Themes are applied via `data-theme` attribute on `<html>` tag

### Component Usage

Use DaisyUI components for standard UI elements:
- Buttons: `btn btn-primary`, `btn btn-accent`
- Cards: `card bg-base-200 shadow-xl`
- Inputs: `input input-bordered`, `file-input file-input-bordered`
- Chat: `chat chat-start`, `chat chat-end`, `chat-bubble`
- Progress: `progress progress-primary`
- Alerts: `alert alert-error`, `alert alert-success`
- Loading: `loading loading-spinner`

### Responsive Design

Use Tailwind's mobile-first breakpoints:
- `sm:` (640px+), `md:` (768px+), `lg:` (1024px+), `xl:` (1280px+)
- Example: `flex flex-col lg:flex-row` (stack on mobile, row on desktop)

### Custom Effects

Preserve unique visual effects in custom CSS:
- Blood drip animations (Ouija Board)
- Mystical fog overlay (Ouija Board)
- Planchette cursor (Ouija Board)
- Title pulse animations (both themes)

### Accessibility

All components meet WCAG AA standards:
- Minimum 44x44px touch targets: `min-h-[44px] min-w-[44px]`
- High color contrast ratios (14.5:1 Legal, 18.2:1 Ouija)
- Visible focus indicators (DaisyUI built-in)
- Semantic HTML with ARIA labels
