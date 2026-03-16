from langchain_tavily import TavilySearch
from dotenv import load_dotenv
import os

load_dotenv()  # this must run before you call os.getenv

tavily_api_key = os.getenv("TAVILY_API_KEY")

if not tavily_api_key:
    raise ValueError("TAVILY_API_KEY not found. Add it to your .env file or environment variables.")

search_tool = TavilySearch(
    tavily_api_key=tavily_api_key,
    max_results=3
)