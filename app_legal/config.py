"""Configuration for App 1: The Legal Eagle"""

class Config:
    # Branding
    APP_NAME = "Legal Eagle ⚖️"
    THEME_CSS = "blue-corporate"
    
    # DaisyUI Theme Configuration
    DAISYUI_THEME = "legal-eagle"
    DAISYUI_THEME_CONFIG = {
        "legal-eagle": {
            "primary": "#0f172a",      # Deep slate navy
            "secondary": "#334155",    # Steel grey
            "accent": "#ca8a04",       # Muted gold
            "neutral": "#1e293b",      # Dark slate
            "base-100": "#f8fafc",     # Light grey background
            "base-200": "#f1f5f9",     # Input background
            "base-300": "#e2e8f0",     # Border color
            "info": "#3b82f6",
            "success": "#10b981",
            "warning": "#f59e0b",
            "error": "#ef4444"
        }
    }
    
    # RAG Configuration
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    TOP_K_RESULTS = 3
    RELEVANCE_THRESHOLD = 0.3  # Distance threshold for filtering results
    
    # AI Personality
    SYSTEM_PROMPT = """
    You are 'Legal Eagle', an AI legal assistant designed to analyze documents with extreme precision.
    
    RULES:
    1. You MUST answer strictly based on the provided CONTEXT INFORMATION.
    2. If the answer is not in the text, state "This information is not present in the document."
    3. Use professional, formal legal terminology.
    4. Cite specific snippets or sections from the context to support your answer.
    5. Do not use emojis or informal language.
    """