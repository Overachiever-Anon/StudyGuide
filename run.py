import os
from dotenv import load_dotenv

# Load environment variables from the root .env file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

from backend import create_app

app = create_app()

if __name__ == "__main__":
    # This port is for local development; Gunicorn will use the port from the Dockerfile in production.
    app.run(host="0.0.0.0", port=5001, debug=True)
