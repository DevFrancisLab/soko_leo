from tools.tavily_tool import search_tool
from langchain.chat_models import init_chat_model
import os

# Set Vertex AI API key
os.environ["GOOGLE_API_KEY"] = os.getenv("VERTEX_AI_API_KEY")

llm = init_chat_model("google_genai:gemini-1.5-pro")

def market_news_agent(state):

    question = state["messages"][-1].content

    results = search_tool.invoke(
        f"Kenya agriculture news {question}"
    )

    prompt = f"""
Explain the following agricultural news for Kenyan farmers.

{results}
"""

    response = llm.invoke(prompt)

    return {"messages":[response]}