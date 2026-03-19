"""
Google Gemini API Client Module

This module provides a simple interface to interact with Google's Gemini model
using the google-generativeai library directly.

Environment Variables:
- VERTEX_AI_API_KEY: Your Google Generative AI API Key
"""

import os
from pathlib import Path


def load_env():
    """Load environment variables from .env file."""
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        env_path = Path(__file__).resolve().parent / ".env"
    
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, _, value = line.partition('=')
                    os.environ.setdefault(key, value.strip('"\''))


# Load environment variables
load_env()

# Get API key
API_KEY = os.getenv("VERTEX_AI_API_KEY")

if not API_KEY:
    print("Warning: VERTEX_AI_API_KEY not found in environment")


def gemini_generate(prompt: str) -> str:
    """
    Generate text using Google Gemini API.

    Args:
        prompt (str): The input prompt for text generation

    Returns:
        str: The generated text response, or empty string if generation fails
    """
    if not API_KEY:
        print("Error: VERTEX_AI_API_KEY not configured")
        return ""
    
    try:
        import google.generativeai as genai
        
        # Configure the API
        genai.configure(api_key=API_KEY)
        
        # Create model and generate content
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        
        # Extract and return text
        if response and hasattr(response, 'text') and response.text:
            return response.text.strip()
        else:
            print("[Gemini] Warning: Empty response from API")
            return ""
            
    except ImportError:
        print("Error: google-generativeai library not installed")
        return ""
    except Exception as e:
        print(f"[Gemini] Error: {e}")
        import traceback
        traceback.print_exc()
        return ""
