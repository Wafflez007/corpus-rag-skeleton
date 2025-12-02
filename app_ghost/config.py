"""Configuration for App 2: The Ouija Board"""

class Config:
    # Branding
    APP_NAME = "Ouija Board 🔮"
    THEME_CSS = "dark-gothic"
    
    # DaisyUI Theme Configuration
    DAISYUI_THEME = "ouija-board"
    DAISYUI_THEME_CONFIG = {
        "ouija-board": {
            "primary": "#8b0000",      # Deep blood red
            "secondary": "#2b0505",    # Dried blood
            "accent": "#ff3f3f",       # Bright red glow
            "neutral": "#d4d4d4",      # Ghostly white
            "base-100": "#050505",     # Void black
            "base-200": "#110a0a",     # Dark card
            "base-300": "#3a1a1a",     # Dark border
            "info": "#8b0000",
            "success": "#8b0000",
            "warning": "#ff3f3f",
            "error": "#ff3f3f"
        }
    }
    
    # RAG Configuration
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    TOP_K_RESULTS = 3
    RELEVANCE_THRESHOLD = 0.3  # Distance threshold for filtering results
    
    # AI Personality
    SYSTEM_PROMPT = """
    You are the 'Spirit of the Ouija Board', a mystical entity that communes with documents from beyond the veil.
    
    RULES:
    1. You MUST answer based on the provided CONTEXT INFORMATION from the summoned documents.
    2. If the answer is not in the text, state "The spirits are silent on this matter..."
    3. Use mysterious, atmospheric language with gothic flair.
    4. Reference the "ancient texts" or "forbidden knowledge" when citing the context.
    5. You may use mystical emojis sparingly (🔮, 💀, 👻, 🕯️).
    6. Speak as if channeling knowledge from another realm.
    """