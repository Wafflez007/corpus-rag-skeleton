"""Unified launcher for both Legal Eagle and Ghost apps"""

import os
import sys
from dotenv import load_dotenv
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from flask import Flask, render_template_string

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from skeleton_core.app import create_app
from app_legal.config import Config as LegalConfig
from app_ghost.config import Config as GhostConfig

load_dotenv()

# Create landing page app
landing_app = Flask(__name__)

LANDING_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Corpus - Choose Your Experience</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            position: relative;
            overflow: hidden;
        }
        
        /* Animated background particles */
        body::before {
            content: '';
            position: absolute;
            width: 200%;
            height: 200%;
            background-image: 
                radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 40% 20%, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
            animation: float 20s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translate(0, 0) rotate(0deg); }
            33% { transform: translate(30px, -30px) rotate(120deg); }
            66% { transform: translate(-20px, 20px) rotate(240deg); }
        }
        
        .container {
            text-align: center;
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(10px);
            padding: 4rem 3rem;
            border-radius: 30px;
            box-shadow: 0 30px 80px rgba(0, 0, 0, 0.3);
            max-width: 900px;
            width: 90%;
            position: relative;
            z-index: 1;
            animation: slideUp 0.6s ease-out;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .logo {
            font-size: 4rem;
            margin-bottom: 1rem;
            animation: bounce 2s ease-in-out infinite;
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        h1 {
            color: #1a1a2e;
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .subtitle {
            color: #666;
            font-size: 1.1rem;
            margin-bottom: 3rem;
            font-weight: 400;
        }
        
        .tagline {
            color: #999;
            font-size: 0.9rem;
            margin-bottom: 2.5rem;
            font-style: italic;
        }
        
        .apps {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }
        
        .app-card {
            position: relative;
            color: white;
            padding: 3rem 2rem;
            border-radius: 20px;
            text-decoration: none;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            overflow: hidden;
            border: 2px solid transparent;
        }
        
        .app-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: inherit;
            transition: transform 0.4s ease;
            z-index: -1;
        }
        
        .app-card:hover::before {
            transform: scale(1.05);
        }
        
        .app-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
            border-color: rgba(255, 255, 255, 0.3);
        }
        
        .app-card.legal {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        }
        
        .app-card.ghost {
            background: linear-gradient(135deg, #2c003e 0%, #4a0e4e 100%);
        }
        
        .app-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
            display: inline-block;
            animation: iconFloat 3s ease-in-out infinite;
        }
        
        @keyframes iconFloat {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            50% { transform: translateY(-8px) rotate(5deg); }
        }
        
        .app-card:hover .app-icon {
            animation: iconSpin 0.6s ease-in-out;
        }
        
        @keyframes iconSpin {
            0% { transform: rotate(0deg) scale(1); }
            50% { transform: rotate(180deg) scale(1.2); }
            100% { transform: rotate(360deg) scale(1); }
        }
        
        .app-name {
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 0.8rem;
            letter-spacing: -0.5px;
        }
        
        .app-desc {
            font-size: 1rem;
            opacity: 0.95;
            line-height: 1.5;
            font-weight: 400;
        }
        
        .app-features {
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid rgba(255, 255, 255, 0.2);
            font-size: 0.85rem;
            opacity: 0.8;
        }
        
        .cta {
            display: inline-block;
            margin-top: 1rem;
            padding: 0.5rem 1.5rem;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .app-card:hover .cta {
            background: rgba(255, 255, 255, 0.3);
            transform: scale(1.05);
        }
        
        .footer {
            margin-top: 2rem;
            padding-top: 2rem;
            border-top: 1px solid #e0e0e0;
            color: #999;
            font-size: 0.85rem;
        }
        
        .tech-badge {
            display: inline-block;
            margin: 0.5rem 0.3rem;
            padding: 0.3rem 0.8rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 2rem 1.5rem;
            }
            
            h1 {
                font-size: 2rem;
            }
            
            .apps {
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }
            
            .app-card {
                padding: 2rem 1.5rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🎭</div>
        <h1>Project Corpus</h1>
        <p class="subtitle">AI-Powered Document Intelligence with Personality</p>
        <p class="tagline">Choose your experience and chat with your documents</p>
        
        <div class="apps">
            <a href="/legal/" class="app-card legal">
                <div class="app-icon">⚖️</div>
                <div class="app-name">Legal Eagle</div>
                <div class="app-desc">Professional legal document analysis with precision and expertise</div>
                <div class="app-features">
                    📄 PDF & Text Support<br>
                    🔍 Semantic Search<br>
                    🤖 AI-Powered Insights
                </div>
                <div class="cta">Enter Legal Mode →</div>
            </a>
            
            <a href="/ghost/" class="app-card ghost">
                <div class="app-icon">👻</div>
                <div class="app-name">Ouija Board</div>
                <div class="app-desc">Mystical document consultation from beyond the veil</div>
                <div class="app-features">
                    🔮 Cryptic Wisdom<br>
                    ✨ Ethereal Insights<br>
                    🌙 Supernatural Analysis
                </div>
                <div class="cta">Summon the Spirits →</div>
            </a>
        </div>
        
        <div class="footer">
            <div>
                <span class="tech-badge">Flask</span>
                <span class="tech-badge">ChromaDB</span>
                <span class="tech-badge">Google Gemini</span>
                <span class="tech-badge">RAG</span>
            </div>
            <p style="margin-top: 1rem;">Powered by Retrieval Augmented Generation</p>
        </div>
    </div>
</body>
</html>
"""

@landing_app.route('/')
def landing():
    return render_template_string(LANDING_PAGE)

# Create both apps
legal_app = create_app(LegalConfig)
ghost_app = create_app(GhostConfig)

# Combine apps using dispatcher
application = DispatcherMiddleware(landing_app, {
    '/legal': legal_app,
    '/ghost': ghost_app
})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🎭 Starting Project Corpus Unified Launcher...")
    print(f"🏠 Landing page: /")
    print(f"⚖️  Legal Eagle: /legal/")
    print(f"👻 Ghost/Ouija: /ghost/")
    print(f"\n🚀 Server running on port {port}\n")
    
    run_simple('0.0.0.0', port, application, use_reloader=False, use_debugger=False)
