import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

def get_anthropic_client():
    """Initializes and returns the Anthropic client."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Warning: ANTHROPIC_API_KEY not found in .env file. AI features will be disabled.")
        return None
    return anthropic.Anthropic(api_key=api_key)
