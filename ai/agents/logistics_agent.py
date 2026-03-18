# agents/logistics_agent.py
from langchain_core.messages import AIMessage

def LogisticsAgent(state: dict):
    location = state.get("location", "Kenya")
    query = state["messages"][-1].content

    advice = (
        f"Logistics Agent Advice:\n"
        f"- Store crops properly to prevent spoilage.\n"
        f"- Use main highways or trusted routes for transport.\n"
        f"- Optimize procurement and delivery timing to match market demand."
    )
    return {"messages":[AIMessage(content=advice)]}