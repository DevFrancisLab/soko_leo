import os

from dotenv import load_dotenv

# Load environment variables from $REPO_ROOT/ai/.env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

LLMAPI_API_KEY = os.getenv("LLMAPI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

missing_keys = [
    k
    for k, v in (
        ("LLMAPI_API_KEY", LLMAPI_API_KEY),
        ("TAVILY_API_KEY", TAVILY_API_KEY),
    )
    if not v
]

if missing_keys:
    raise RuntimeError(f"Missing required environment key(s): {', '.join(missing_keys)}")
