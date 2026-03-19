from dotenv import load_dotenv
import os

from langchain.tools import BaseTool
from langchain_tavily import TavilySearch

load_dotenv()  # this must run before you call os.getenv

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if TAVILY_API_KEY:
    search_tool = TavilySearch(
        tavily_api_key=TAVILY_API_KEY,
        max_results=3,
    )
else:
    class DisabledSearchTool(BaseTool):
        name: str = "tavily_search"
        description: str = "Disabled search tool because TAVILY_API_KEY is not configured."

        def _run(self, query: str) -> str:
            return "Tavily search is disabled because TAVILY_API_KEY is not configured."

        async def _arun(self, query: str) -> str:
            return self._run(query)

    search_tool = DisabledSearchTool()
