"""Flask application factory for the RAG skeleton"""

import json
import logging
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from typing import Any, Generator
from pypdf import PdfReader
from .vector_store import VectorStore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app(config: Any) -> Flask:
    """
    Create and configure the Flask application.
    
    Args:
        config: Configuration object with personality and RAG settings
    """
    app = Flask(__name__)
    
    # Store config in app context
    app.config['APP_NAME'] = config.APP_NAME
    app.config['THEME_CSS'] = config.THEME_CSS
    app.config['SYSTEM_PROMPT'] = config.SYSTEM_PROMPT
    
    # DaisyUI theme configuration (with defaults for backward compatibility)
    app.config['DAISYUI_THEME'] = getattr(config, 'DAISYUI_THEME', None)
    app.config['DAISYUI_THEME_CONFIG'] = getattr(config, 'DAISYUI_THEME_CONFIG', {})
    
    # RAG configuration (with defaults for backward compatibility)
    app.config['CHUNK_SIZE'] = getattr(config, 'CHUNK_SIZE', 500)
    app.config['CHUNK_OVERLAP'] = getattr(config, 'CHUNK_OVERLAP', 50)
    app.config['TOP_K_RESULTS'] = getattr(config, 'TOP_K_RESULTS', 3)
    app.config['RELEVANCE_THRESHOLD'] = getattr(config, 'RELEVANCE_THRESHOLD', 0.3)
    
    # Initialize the Brain (VectorStore) with config
    vector_store = VectorStore(
        chunk_size=app.config['CHUNK_SIZE'],
        chunk_overlap=app.config['CHUNK_OVERLAP']
    )
    
    # Track the active Gemini model (will be set on first use)
    app.config['ACTIVE_MODEL'] = None

    @app.route('/')
    def index():
        """Main page"""
        return render_template(
            'index.html',
            app_name=app.config['APP_NAME'],
            theme=app.config['THEME_CSS'],
            model_name=app.config.get('ACTIVE_MODEL', 'Gemini AI'),
            daisyui_theme=app.config.get('DAISYUI_THEME'),
            daisyui_theme_config=app.config.get('DAISYUI_THEME_CONFIG', {})
        )
    
    @app.route('/upload', methods=['POST'])
    def upload():
        """Handle document upload and vectorization with SSE progress"""
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        def generate_progress() -> Generator[str, None, None]:
            """Generate SSE progress updates"""
            try:
                # Stage 1: Reading file (0-20%)
                yield f"data: {json.dumps({'progress': 10, 'stage': 'reading'})}\n\n"
                
                file_data = []
                
                # Handle PDF files
                if file.filename.lower().endswith('.pdf'):
                    yield f"data: {json.dumps({'progress': 20, 'stage': 'parsing'})}\n\n"
                    pdf = PdfReader(file.stream)
                    total_pages = len(pdf.pages)
                    
                    for i, page in enumerate(pdf.pages):
                        text = page.extract_text()
                        if text.strip():
                            file_data.append({'text': text, 'page': i + 1})
                        
                        # Update progress for each page (20-50%)
                        progress = 20 + int((i + 1) / total_pages * 30)
                        yield f"data: {json.dumps({'progress': progress, 'stage': 'parsing'})}\n\n"
                
                # Handle Text files
                elif file.filename.lower().endswith('.txt'):
                    yield f"data: {json.dumps({'progress': 30, 'stage': 'parsing'})}\n\n"
                    text = file.read().decode('utf-8')
                    file_data.append({'text': text, 'page': 1})
                    yield f"data: {json.dumps({'progress': 50, 'stage': 'parsing'})}\n\n"
                else:
                    yield f"data: {json.dumps({'error': 'Unsupported file type'})}\n\n"
                    return

                if not file_data:
                    yield f"data: {json.dumps({'error': 'File appears empty'})}\n\n"
                    return

                # Stage 2: Vectorizing (50-90%)
                yield f"data: {json.dumps({'progress': 60, 'stage': 'vectorizing'})}\n\n"
                
                num_chunks = vector_store.ingest_document(
                    file_data=file_data, 
                    document_id=file.filename, 
                    metadata={}
                )
                
                yield f"data: {json.dumps({'progress': 90, 'stage': 'finalizing'})}\n\n"
                
                # Stage 3: Complete (100%)
                total_pages = len(file_data)
                yield f"data: {json.dumps({'progress': 100, 'stage': 'complete', 'filename': file.filename, 'chunks_processed': num_chunks, 'pages': total_pages, 'message': f'Successfully memorized {num_chunks} fragments.'})}\n\n"

            except Exception as e:
                logger.error(f"Error processing file: {e}", exc_info=True)
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

        return Response(stream_with_context(generate_progress()), mimetype='text/event-stream')
    
    @app.route('/documents', methods=['GET'])
    def list_documents():
        """List all uploaded documents"""
        try:
            docs = vector_store.list_documents()
            return jsonify({'documents': docs})
        except Exception as e:
            logger.error(f"Error listing documents: {e}", exc_info=True)
            return jsonify({'error': str(e)}), 500
    
    @app.route('/documents/<path:source>', methods=['DELETE'])
    def delete_document(source):
        """Delete a specific document"""
        try:
            deleted_count = vector_store.delete_document(source)
            return jsonify({'success': True, 'deleted_chunks': deleted_count})
        except Exception as e:
            logger.error(f"Error deleting document: {e}", exc_info=True)
            return jsonify({'error': str(e)}), 500
    
    @app.route('/chat', methods=['POST'])
    def chat():
        """Handle chat queries with RAG and Personality"""
        data = request.json
        query = data.get('query')
        selected_sources = data.get('sources', None)  # Optional filter
        if not query:
            return jsonify({'error': 'No query provided'}), 400
            
        # 1. Retrieve Context from Brain (with optional source filter)
        context_results = vector_store.search(
            query, 
            n_results=app.config['TOP_K_RESULTS'], 
            filter_sources=selected_sources
        )
        
        # Filter results to only include truly relevant sources
        # Only keep results within a reasonable distance threshold of the best match
        if context_results and len(context_results) > 0:
            best_distance = context_results[0].get('distance', 0)
            threshold = app.config['RELEVANCE_THRESHOLD']
            # Keep results within threshold distance units of the best match
            # This filters out weakly-related documents
            context_results = [r for r in context_results if r.get('distance', 0) <= best_distance + threshold]
        
        context_text = "\n\n".join([r['text'] for r in context_results])
        
        # 2. Construct the Prompt
        system_prompt = app.config['SYSTEM_PROMPT']
        full_prompt = f"""
        INSTRUCTIONS: {system_prompt}
        
        CONTEXT INFORMATION (Use this to answer):
        {context_text}
        
        USER QUESTION:
        {query}
        
        ANSWER:
        """
        
        # 3. Robust Model Selection (Prioritize Flash)
        try:
            # Explicitly try the most common free/fast models in order
            candidates = [
                'gemini-1.5-flash',
                'gemini-1.5-flash-latest',
                'gemini-1.5-flash-001',
                'gemini-1.0-pro',
                'gemini-pro'
            ]
            
            response = None
            used_model = None
            for model_name in candidates:
                try:
                    logger.info(f"Trying model: {model_name}")
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(full_prompt)
                    used_model = model_name
                    logger.info(f"Successfully using model: {model_name}")
                    app.config['ACTIVE_MODEL'] = model_name
                    break  # It worked! Exit loop
                except Exception as e:
                    logger.debug(f"Model {model_name} failed: {e}")
                    continue  # Try next one
            
            if not response:
                # Last resort: Pick ANY valid model, but avoid 'exp' or 'pro' if possible
                logger.warning("Standard models failed. Searching available list...")
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        if 'flash' in m.name:  # Prefer flash
                            model = genai.GenerativeModel(m.name)
                            response = model.generate_content(full_prompt)
                            used_model = m.name
                            app.config['ACTIVE_MODEL'] = m.name
                            logger.info(f"Using fallback model: {m.name}")
                            break
            
            # If still nothing, grab the very first one
            if not response:
                try:
                    first_model = list(genai.list_models())[0].name
                    model = genai.GenerativeModel(first_model)
                    response = model.generate_content(full_prompt)
                    used_model = first_model
                    app.config['ACTIVE_MODEL'] = first_model
                    logger.info(f"Using last resort model: {first_model}")
                except Exception as e:
                    logger.error(f"Critical Model Failure: {e}", exc_info=True)
                    return jsonify({'error': 'AI Service Unavailable'}), 503

            # 4. Safe Text Extraction (The Fix for IndexError)
            ai_text = "..."
            try:
                if response and response.candidates:
                    ai_text = response.text
                else:
                    ai_text = "The spirits are silent. (Safety filter triggered or empty response)"
            except ValueError:
                # Gemini raises ValueError if the response was blocked by safety filters
                ai_text = "🤐 [Response Redacted by Safety Filters]. Try asking differently."

            return jsonify({
                'status': 'success',
                'echo': ai_text,
                'sources': [r['metadata'] for r in context_results]
            })
                    
        except Exception as e:
            # If we still hit a rate limit, show a friendly error
            if "429" in str(e):
                logger.warning(f"Rate limit exceeded for query: {query[:50]}...")
                return jsonify({'error': 'Rate limit exceeded. Please wait 1 minute.'}), 429
            logger.error(f"Chat Error: {e}", exc_info=True)
            return jsonify({'error': str(e)}), 500
    
    return app