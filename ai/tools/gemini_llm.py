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


def gemini_generate(prompt: str) -> str:
    """
    Generate text using Google Gemini API.

    Args:
        prompt (str): The input prompt for text generation

    Returns:
        str: The generated text response, or empty string if generation fails
    """
    # Reload .env on each call to ensure the key is available even if the
    # module was imported before the environment was populated.
    load_env()

    api_key = os.getenv("VERTEX_AI_API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: VERTEX_AI_API_KEY/GOOGLE_API_KEY/GEMINI_API_KEY not configured")
        return ""
    
    try:
        import google.generativeai as genai
        
        # Configure the API
        genai.configure(api_key=api_key)
        
        # Create model and generate content
        model = genai.GenerativeModel("gemini-1.5-flash")
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
