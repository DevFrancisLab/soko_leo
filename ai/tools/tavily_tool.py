from langchain_tavily import TavilySearch
from dotenv import load_dotenv
import os

load_dotenv()  # this must run before you call os.getenv

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise EnvironmentError("Please set TAVILY_API_KEY in your .env file")

search_tool = TavilySearch(
    tavily_api_key=TAVILY_API_KEY,
    max_results=3
)