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

# Enhanced Landing Page with Split-Screen Architecture
LANDING_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Corpus | Select Domain</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Creepster&family=Inter:wght@300;400;600&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
    <style>
        :root {
            --legal-blue: #0f172a;
            --legal-gold: #c5a059;
            --ghost-dark: #0a0118;
            --ghost-glow: #b026ff;
            --split-speed: 1000ms;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', sans-serif;
            overflow: hidden; /* Hide scrollbars */
            height: 100vh;
            background: #111;
        }

        /* CONTAINER */
        .container {
            position: relative;
            width: 100%;
            height: 100%;
            display: flex;
        }

        /* SPLIT SECTIONS */
        .split {
            position: relative;
            width: 50%;
            height: 100%;
            overflow: hidden;
            transition: width var(--split-speed) ease-in-out;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            cursor: pointer;
        }

        /* BACKGROUND CONTENT LAYERS */
        .bg-layer {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
        }

        .content {
            position: relative;
            z-index: 10;
            text-align: center;
            transform: translateY(0);
            transition: transform var(--split-speed) ease-in-out;
            padding: 2rem;
            max-width: 600px;
        }

        /* HEADINGS & TEXT */
        h1 {
            font-size: 4rem;
            margin-bottom: 0.5rem;
            white-space: nowrap;
        }

        p.desc {
            font-size: 1.2rem;
            line-height: 1.6;
            opacity: 0; /* Hidden by default */
            transform: translateY(20px);
            transition: all 0.5s ease-in-out;
            max-width: 400px;
            margin: 0 auto;
        }

        .btn {
            display: inline-block;
            margin-top: 2rem;
            padding: 1rem 2.5rem;
            border-radius: 50px;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: bold;
            font-size: 0.9rem;
            transition: all 0.3s;
            opacity: 0;
            transform: translateY(20px);
        }

        /* --- LEGAL SIDE STYLING --- */
        .split.legal {
            background-color: var(--legal-blue);
            color: #fff;
            border-right: 2px solid var(--legal-gold);
        }

        /* Architectural Grid Pattern */
        .split.legal .bg-layer {
            background-image: 
                linear-gradient(rgba(197, 160, 89, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(197, 160, 89, 0.05) 1px, transparent 1px);
            background-size: 40px 40px;
            animation: scrollGrid 60s linear infinite;
        }

        .split.legal h1 {
            font-family: 'Playfair Display', serif;
            color: var(--legal-gold);
            text-shadow: 0 2px 10px rgba(0,0,0,0.5);
        }

        .split.legal .icon {
            font-size: 5rem;
            margin-bottom: 1rem;
            filter: drop-shadow(0 0 10px rgba(197, 160, 89, 0.3));
        }

        .split.legal .btn {
            border: 1px solid var(--legal-gold);
            color: var(--legal-gold);
            background: rgba(15, 23, 42, 0.8);
        }

        .split.legal:hover .btn {
            background: var(--legal-gold);
            color: var(--legal-blue);
        }

        /* --- GHOST SIDE STYLING --- */
        .split.ghost {
            background-color: var(--ghost-dark);
            color: #e0e0e0;
        }

        /* Fog Animation */
        .split.ghost .bg-layer {
            background: 
                radial-gradient(circle at 50% 50%, rgba(75, 0, 130, 0.2), transparent 70%),
                url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.05'/%3E%3C/svg%3E");
        }
        
        .split.ghost::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(45deg, transparent 40%, rgba(176, 38, 255, 0.1) 100%);
            animation: pulseGlow 4s ease-in-out infinite alternate;
        }

        .split.ghost h1 {
            font-family: 'Creepster', display;
            letter-spacing: 3px;
            color: #d8b4fe;
            text-shadow: 0 0 15px var(--ghost-glow);
        }

        .split.ghost .icon {
            font-size: 5rem;
            margin-bottom: 1rem;
            animation: float 6s ease-in-out infinite;
        }

        .split.ghost .btn {
            border: 1px solid #d8b4fe;
            color: #d8b4fe;
            background: rgba(10, 1, 24, 0.8);
            box-shadow: 0 0 10px var(--ghost-glow);
        }

        .split.ghost:hover .btn {
            background: #d8b4fe;
            color: var(--ghost-dark);
            box-shadow: 0 0 20px var(--ghost-glow);
        }

        /* --- INTERACTION CLASSES --- */
        
        /* When hovering Left */
        .hover-left .split.legal { width: 75%; }
        .hover-left .split.ghost { width: 25%; }
        
        /* When hovering Right */
        .hover-right .split.ghost { width: 75%; }
        .hover-right .split.legal { width: 25%; }

        /* Show details on active side */
        .hover-left .split.legal .desc,
        .hover-left .split.legal .btn,
        .hover-right .split.ghost .desc,
        .hover-right .split.ghost .btn {
            opacity: 1;
            transform: translateY(0);
            transition-delay: 0.1s;
        }

        /* Dim passive side */
        .hover-left .split.ghost h1,
        .hover-left .split.ghost .icon { opacity: 0.5; transform: scale(0.8); }
        .hover-right .split.legal h1,
        .hover-right .split.legal .icon { opacity: 0.5; transform: scale(0.8); }

        /* --- ANIMATIONS --- */
        @keyframes scrollGrid {
            0% { background-position: 0 0; }
            100% { background-position: 0 1000px; }
        }

        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }

        @keyframes pulseGlow {
            0% { opacity: 0.3; }
            100% { opacity: 0.7; }
        }

        /* --- MOBILE RESPONSIVE --- */
        @media(max-width: 800px) {
            .container { flex-direction: column; }
            .split { width: 100% !important; height: 50%; }
            
            /* Mobile Hover Simulation (Click/Tap states) */
            .split:hover { height: 60%; }
            .split:not(:hover) { height: 40%; }
            
            h1 { font-size: 2.5rem; }
            .icon { font-size: 3rem; }
            p.desc { display: none; } /* Hide description on mobile to save space */
            .btn { opacity: 1; transform: translateY(0); margin-top: 1rem; padding: 0.8rem 1.5rem; }
        }
    </style>
</head>
<body>

    <div class="container">
        
        <!-- LEGAL SIDE -->
        <a href="/legal/" class="split legal">
            <div class="bg-layer"></div>
            <div class="content">
                <div class="icon">⚖️</div>
                <h1>Legal Eagle</h1>
                <p class="desc">
                    Precision. Precedent. Professionalism.<br>
                    Analyze contracts and case law with <br>rigorous semantic search.
                </p>
                <div class="btn">Access Counsel</div>
            </div>
        </a>

        <!-- GHOST SIDE -->
        <a href="/ghost/" class="split ghost">
            <div class="bg-layer"></div>
            <div class="content">
                <div class="icon">🔮</div>
                <h1>Ouija Board</h1>
                <p class="desc">
                    Consult the archives from beyond the veil.<br>
                    Unearth hidden meanings and <br>cryptic connections.
                </p>
                <div class="btn">Summon Spirits</div>
            </div>
        </a>

    </div>

    <script>
        const container = document.querySelector('.container');
        const legal = document.querySelector('.split.legal');
        const ghost = document.querySelector('.split.ghost');

        // Add hover classes to container for CSS width transitions
        legal.addEventListener('mouseenter', () => container.classList.add('hover-left'));
        legal.addEventListener('mouseleave', () => container.classList.remove('hover-left'));

        ghost.addEventListener('mouseenter', () => container.classList.add('hover-right'));
        ghost.addEventListener('mouseleave', () => container.classList.remove('hover-right'));
    </script>
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