# agents/profit_agent.py
from langchain_core.messages import AIMessage

def ProfitAgent(state: dict):
    location = state.get("location", "Kenya")
    season = state.get("season", "current")
    query = state["messages"][-1].content

    advice = (
        f"Profit Agent Advice:\n"
        f"- Consider crops in high demand in {location} this {season} season.\n"
        f"- Diversify to mitigate risk and maximize profits.\n"
        f"- Check current market prices before selling."
    )
    return {"messages":[AIMessage(content=advice)]}