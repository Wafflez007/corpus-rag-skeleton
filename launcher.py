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
<html>
<head>
    <title>Project Corpus - Choose Your Experience</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .container {
            text-align: center;
            background: white;
            padding: 3rem;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 600px;
        }
        h1 {
            color: #333;
            margin-bottom: 1rem;
        }
        .subtitle {
            color: #666;
            margin-bottom: 2rem;
        }
        .apps {
            display: flex;
            gap: 2rem;
            justify-content: center;
            flex-wrap: wrap;
        }
        .app-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            text-decoration: none;
            transition: transform 0.3s, box-shadow 0.3s;
            min-width: 200px;
        }
        .app-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .app-card.legal {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        }
        .app-card.ghost {
            background: linear-gradient(135deg, #2c003e 0%, #4a0e4e 100%);
        }
        .app-icon {
            font-size: 3rem;
            margin-bottom: 0.5rem;
        }
        .app-name {
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .app-desc {
            font-size: 0.9rem;
            opacity: 0.9;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎭 Project Corpus</h1>
        <p class="subtitle">Choose your AI personality experience</p>
        <div class="apps">
            <a href="/legal/" class="app-card legal">
                <div class="app-icon">⚖️</div>
                <div class="app-name">Legal Eagle</div>
                <div class="app-desc">Professional legal document analysis</div>
            </a>
            <a href="/ghost/" class="app-card ghost">
                <div class="app-icon">👻</div>
                <div class="app-name">Ouija Board</div>
                <div class="app-desc">Mystical document consultation</div>
            </a>
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
