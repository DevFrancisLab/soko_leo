# agents/weather_agent.py
from langchain_core.messages import AIMessage

def WeatherAgent(state: dict):
    location = state.get("location", "Kenya")
    season = state.get("season", "current")
    
    advice = (
        f"Weather Agent Advice:\n"
        f"- Monitor weather patterns in {location}.\n"
        f"- Plant drought-resistant crops if rainfall is low.\n"
        f"- Harvest early if rains are delayed or unpredictable."
    )
    return {"messages":[AIMessage(content=advice)]}