from dataclasses import dataclass
from typing import Any, Dict, Tuple

import requests

from .config import LLMAPI_API_KEY, TAVILY_API_KEY


@dataclass
class Thought:
    """A reasoning step taken by the agent."""

    text: str


@dataclass
class Action:
    """An action the agent wants to perform."""

    name: str
    params: Dict[str, Any]


def combined_market_insight(market_data: str) -> str:
    """Call LLMAPI (gemini-3.1-pro-preview) and Tavily model, then merge outputs.

    This function makes simple HTTP requests to the two services using the
    configured API keys and returns a combined, actionable insight string.
    """

    # --- LLMAPI call (Gemini 3.1 Pro Preview) ---
    llm_response = ""
    try:
        llm_payload = {
            "model": "gemini-3.1-pro-preview",
            "input": market_data,
        }
        llm_headers = {
            "Authorization": f"Bearer {LLMAPI_API_KEY}",
            "Content-Type": "application/json",
        }
        llm_res = requests.post("https://api.llmapi.com/v1/generate", json=llm_payload, headers=llm_headers, timeout=10)
        llm_res.raise_for_status()
        llm_response = llm_res.json().get("output", "")
    except Exception:
        llm_response = "(LLMAPI response unavailable)"

    # --- Tavily call ---
    tavily_response = ""
    try:
        tavily_payload = {
            "model": "tavily-default",
            "prompt": market_data,
        }
        tavily_headers = {
            "Authorization": f"Bearer {TAVILY_API_KEY}",
            "Content-Type": "application/json",
        }
        tavily_res = requests.post("https://api.tavily.ai/v1/complete", json=tavily_payload, headers=tavily_headers, timeout=10)
        tavily_res.raise_for_status()
        tavily_response = tavily_res.json().get("result", "")
    except Exception:
        tavily_response = "(Tavily response unavailable)"

    combined = (
        "Actionable insight based on market data:\n"
        f"- LLMAPI (Gemini): {llm_response}\n"
        f"- Tavily: {tavily_response}\n"
    )
    return combined


class WeatherAgent:
    """A simple ReAct-style agent that processes weather data and updates state."""

    def __init__(self, llm_api_key: str = LLMAPI_API_KEY, tavily_api_key: str = TAVILY_API_KEY):
        self.llm_api_key = llm_api_key
        self.tavily_api_key = tavily_api_key

    def react(self, weather_data: Dict[str, Any], state: Dict[str, Any]) -> Tuple[Thought, Action]:
        """Analyze weather data and generate a Thought + Action for state updates."""

        thought_text = (
            "I need to interpret the incoming weather data and generate a market-insight "
            "action that updates the workflow state."
        )
        thought = Thought(text=thought_text)

        insight = combined_market_insight(weather_data, self.llm_api_key, self.tavily_api_key)

        # Update state with the latest insight
        state["last_market_insight"] = insight

        action = Action(name="store_market_insight", params={"insight": insight})

        return thought, action
