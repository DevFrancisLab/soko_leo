# agents/market_agent.py
from ai.tools.tavily_tool import search_tool
from langchain_core.messages import AIMessage

def MarketAgent(state: dict):
    query = state["messages"][-1].content
    # Ask Tavily for current market prices
    try:
        results = search_tool({"query": query, "topic": "agriculture"})
        answer = "Market Agent Advice:\n"
        for r in results:
            answer += f"- {r['title']}: {r['snippet']}\n"
    except Exception as e:
        answer = f"[MarketAgent failed]: {str(e)}"
    
    return {"messages":[AIMessage(content=answer)]}