"""
EduForge Backend Application Entry Point
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure the project root is on the Python path
# This allows `from backend import create_app` to work correctly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import create_app

# The Flask app instance is now created only when this script is run directly.
# A WSGI server like Gunicorn will import `create_app` and create the instance itself.
if __name__ == '__main__':
    app = create_app()
    # Note: The debug flag should be False in a production environment
    app.run(host='0.0.0.0', port=5001, debug=True)
