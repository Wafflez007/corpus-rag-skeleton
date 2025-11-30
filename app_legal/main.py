"""Legal Eagle Application Entry Point"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path to import skeleton_core
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skeleton_core.app import create_app
from app_legal.config import Config

# Load environment variables
load_dotenv()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("⚖️  Starting Legal Eagle Application...")
    print(f"📋 App Name: {Config.APP_NAME}")
    print(f"🎨 Theme: {Config.THEME_CSS}")
    print(f"🤖 System Prompt: {Config.SYSTEM_PROMPT[:50]}...")
    print(f"\n🚀 Server running on port {port}\n")
    
    app = create_app(Config)
    app.run(debug=False, host='0.0.0.0', port=port)
