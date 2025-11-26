"""Ghost/Ouija Board Application Entry Point"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path to import skeleton_core
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skeleton_core.app import create_app
from app_ghost.config import Config

# Load environment variables
load_dotenv()

if __name__ == '__main__':
    print("👻 Starting Ouija Board Application...")
    print(f"🔮 App Name: {Config.APP_NAME}")
    print(f"🎨 Theme: {Config.THEME_CSS}")
    print(f"🤖 System Prompt: {Config.SYSTEM_PROMPT[:50]}...")
    print(f"\n🚀 Server running at http://127.0.0.1:5001\n")
    
    app = create_app(Config)
    app.run(debug=True, host='0.0.0.0', port=5001)
