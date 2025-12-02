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

# Enhanced Landing Page with Split-Screen Architecture - Migrated to Tailwind + DaisyUI
LANDING_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Corpus | Select Domain</title>
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- DaisyUI -->
    <link href="https://cdn.jsdelivr.net/npm/daisyui@4.4.19/dist/full.min.css" rel="stylesheet" type="text/css" />
    
    <!-- Tailwind Configuration -->
    <script>
      tailwind.config = {
        theme: {
          extend: {
            colors: {
              'legal-navy': '#0f172a',
              'legal-gold': '#ca8a04',
              'legal-steel': '#334155',
              'legal-slate': '#1e293b',
              'legal-light': '#f8fafc',
              'legal-input': '#f1f5f9',
              'legal-border': '#e2e8f0',
              'ghost-dark': '#050505',
              'ghost-card': '#110a0a',
              'ghost-border': '#3a1a1a',
              'ghost-glow': '#ff3f3f',
              'ghost-blood': '#8b0000',
              'ghost-dried': '#2b0505',
              'ghost-white': '#d4d4d4'
            }
          }
        }
      }
    </script>
    
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Creepster&family=Inter:wght@300;400;600&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
    <style>
        /* Minimal custom CSS for unique effects that can't be replicated with Tailwind */
        
        /* Architectural Grid Pattern Animation for Legal Side */
        .legal-grid-bg {
            background-image: 
                linear-gradient(rgba(197, 160, 89, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(197, 160, 89, 0.05) 1px, transparent 1px);
            background-size: 40px 40px;
            animation: scrollGrid 60s linear infinite;
        }

        /* Mystical Fog Effect for Ghost Side */
        .ghost-fog-bg {
            background: 
                radial-gradient(circle at 50% 50%, rgba(75, 0, 130, 0.2), transparent 70%),
                url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.05'/%3E%3C/svg%3E");
        }
        
        .ghost-glow-overlay::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(45deg, transparent 40%, rgba(176, 38, 255, 0.1) 100%);
            animation: pulseGlow 4s ease-in-out infinite alternate;
            pointer-events: none;
        }

        /* Animations */
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
    </style>
</head>
<body class="font-['Inter'] overflow-hidden h-screen bg-gray-900">

    <!-- Mobile: Single column (stacked), Tablet+: Side-by-side split -->
    <div class="relative w-full h-full flex flex-col md:flex-row" id="container">
        
        <!-- LEGAL SIDE -->
        <a href="/legal/" 
           class="group relative flex-1 overflow-hidden flex items-center justify-center no-underline cursor-pointer bg-legal-navy text-white border-b-2 md:border-b-0 md:border-r-2 border-legal-gold transition-all duration-1000 ease-in-out hover:flex-[1.5] md:hover:flex-[2]"
           id="legal-side">
            <!-- Background Layer -->
            <div class="legal-grid-bg absolute top-0 left-0 w-full h-full z-0"></div>
            
            <!-- Content -->
            <div class="relative z-10 text-center p-6 sm:p-8 max-w-2xl transition-transform duration-1000 ease-in-out">
                <div class="text-6xl sm:text-7xl md:text-8xl mb-3 sm:mb-4 drop-shadow-[0_0_10px_rgba(197,160,89,0.3)] transition-all duration-300 group-hover:scale-100">
                    ⚖️
                </div>
                <h1 class="font-['Playfair_Display'] text-3xl sm:text-4xl md:text-5xl lg:text-6xl mb-2 text-legal-gold" style="text-shadow: 0 2px 10px rgba(0,0,0,0.5);">
                    Legal Eagle
                </h1>
                <p class="text-base sm:text-lg md:text-xl leading-relaxed max-w-md mx-auto opacity-70 md:opacity-0 translate-y-0 md:translate-y-5 transition-all duration-500 ease-in-out md:group-hover:opacity-100 md:group-hover:translate-y-0 delay-100 mt-2 md:mt-0">
                    Precision. Precedent. Professionalism.<br class="hidden sm:inline">
                    Analyze contracts and case law with<br class="hidden sm:inline">rigorous semantic search.
                </p>
                <button class="btn btn-outline border-legal-gold text-legal-gold bg-legal-navy/80 hover:bg-legal-gold hover:text-legal-navy hover:border-legal-gold mt-4 sm:mt-6 md:mt-8 px-8 sm:px-10 rounded-full uppercase tracking-widest font-bold text-xs sm:text-sm transition-all duration-300 opacity-100 md:opacity-0 translate-y-0 md:translate-y-5 md:group-hover:opacity-100 md:group-hover:translate-y-0 delay-100 min-h-[44px] min-w-[44px]">
                    Access Counsel
                </button>
            </div>
        </a>

        <!-- GHOST SIDE -->
        <a href="/ghost/" 
           class="ghost-glow-overlay group relative flex-1 overflow-hidden flex items-center justify-center no-underline cursor-pointer bg-ghost-dark text-gray-200 transition-all duration-1000 ease-in-out hover:flex-[1.5] md:hover:flex-[2]"
           id="ghost-side">
            <!-- Background Layer -->
            <div class="ghost-fog-bg absolute top-0 left-0 w-full h-full z-0"></div>
            
            <!-- Content -->
            <div class="relative z-10 text-center p-6 sm:p-8 max-w-2xl transition-transform duration-1000 ease-in-out">
                <div class="text-6xl sm:text-7xl md:text-8xl mb-3 sm:mb-4 animate-[float_6s_ease-in-out_infinite] transition-all duration-300 group-hover:scale-100">
                    🔮
                </div>
                <h1 class="font-['Creepster'] text-3xl sm:text-4xl md:text-5xl lg:text-6xl mb-2 tracking-wider text-purple-300" style="text-shadow: 0 0 15px #b026ff;">
                    Ouija Board
                </h1>
                <p class="text-base sm:text-lg md:text-xl leading-relaxed max-w-md mx-auto opacity-70 md:opacity-0 translate-y-0 md:translate-y-5 transition-all duration-500 ease-in-out md:group-hover:opacity-100 md:group-hover:translate-y-0 delay-100 mt-2 md:mt-0">
                    Consult the archives from beyond the veil.<br class="hidden sm:inline">
                    Unearth hidden meanings and<br class="hidden sm:inline">cryptic connections.
                </p>
                <button class="btn btn-outline border-purple-300 text-purple-300 bg-[#0a0118]/80 hover:bg-purple-300 hover:text-ghost-dark hover:border-purple-300 shadow-[0_0_10px_#b026ff] hover:shadow-[0_0_20px_#b026ff] mt-4 sm:mt-6 md:mt-8 px-8 sm:px-10 rounded-full uppercase tracking-widest font-bold text-xs sm:text-sm transition-all duration-300 opacity-100 md:opacity-0 translate-y-0 md:translate-y-5 md:group-hover:opacity-100 md:group-hover:translate-y-0 delay-100 min-h-[44px] min-w-[44px]">
                    Summon Spirits
                </button>
            </div>
        </a>

    </div>

    <script>
        // Enhanced hover interaction for desktop
        const container = document.getElementById('container');
        const legalSide = document.getElementById('legal-side');
        const ghostSide = document.getElementById('ghost-side');

        // Dim the non-hovered side on desktop
        legalSide.addEventListener('mouseenter', () => {
            if (window.innerWidth >= 768) {
                ghostSide.querySelector('h1').style.opacity = '0.5';
                ghostSide.querySelector('h1').style.transform = 'scale(0.8)';
                ghostSide.querySelectorAll('.text-7xl, .text-8xl').forEach(el => {
                    el.style.opacity = '0.5';
                    el.style.transform = 'scale(0.8)';
                });
            }
        });

        legalSide.addEventListener('mouseleave', () => {
            if (window.innerWidth >= 768) {
                ghostSide.querySelector('h1').style.opacity = '1';
                ghostSide.querySelector('h1').style.transform = 'scale(1)';
                ghostSide.querySelectorAll('.text-7xl, .text-8xl').forEach(el => {
                    el.style.opacity = '1';
                    el.style.transform = 'scale(1)';
                });
            }
        });

        ghostSide.addEventListener('mouseenter', () => {
            if (window.innerWidth >= 768) {
                legalSide.querySelector('h1').style.opacity = '0.5';
                legalSide.querySelector('h1').style.transform = 'scale(0.8)';
                legalSide.querySelectorAll('.text-7xl, .text-8xl').forEach(el => {
                    el.style.opacity = '0.5';
                    el.style.transform = 'scale(0.8)';
                });
            }
        });

        ghostSide.addEventListener('mouseleave', () => {
            if (window.innerWidth >= 768) {
                legalSide.querySelector('h1').style.opacity = '1';
                legalSide.querySelector('h1').style.transform = 'scale(1)';
                legalSide.querySelectorAll('.text-7xl, .text-8xl').forEach(el => {
                    el.style.opacity = '1';
                    el.style.transform = 'scale(1)';
                });
            }
        });

        // Add smooth transitions
        document.querySelectorAll('h1, .text-7xl, .text-8xl').forEach(el => {
            el.style.transition = 'opacity 0.3s ease-in-out, transform 0.3s ease-in-out';
        });
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