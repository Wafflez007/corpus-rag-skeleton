# Product Overview

This is "Project Corpus" - a RAG (Retrieval Augmented Generation) web application that allows users to chat with uploaded documents. The core feature is its ability to switch personalities and themes based on configuration.

## Key Capabilities

- Upload text/PDF documents and chat with their content
- Vector-based semantic search for relevant context retrieval using ChromaDB
- Configurable AI personalities via system prompts
- Theme-based UI customization
- Page-aware document chunking with source tracking

## Application Modes

The system supports multiple app configurations (e.g., "Legal Eagle" for professional legal analysis, "Ouija Board" for mystical/spooky interactions). Each mode has:
- Distinct system prompts that shape AI behavior
- Custom UI themes and styling
- Unique branding (APP_NAME)
- Independent Flask servers running on different ports

## Architecture Philosophy

The project follows a "skeleton + apps" pattern where `skeleton_core` contains reusable RAG logic, and individual app folders (like `app_legal`, `app_ghost`) provide configuration overlays. Each app has its own `main.py` entry point that imports the core and applies its config.
