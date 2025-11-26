import sys
import os

# Add the parent directory to sys.path so we can find 'skeleton_core'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from skeleton_core.app import create_app
from app_legal.config import Config

# Load env vars (API keys)
load_dotenv()

# Initialize the Legal App
app = create_app(Config)

if __name__ == '__main__':
    print(f"🏛️  Starting {Config.APP_NAME}...")
    print(f"🚀 Server running at http://127.0.0.1:5001")
    # Run on Port 5001 to distinguish it
    app.run(debug=True, host='0.0.0.0', port=5001)