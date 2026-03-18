from tools.tavily_tool import search_tool
from langchain.chat_models import init_chat_model
import os

# Set Vertex AI API key
os.environ["GOOGLE_API_KEY"] = os.getenv("VERTEX_AI_API_KEY")

llm = init_chat_model("google_genai:gemini-1.5-pro")

def market_finder_agent(state):

    question = state["messages"][-1].content

    results = search_tool.invoke(
        f"best market to sell crops Kenya {question}"
    )

    prompt = f"""
Based on this data, recommend the best markets.

{results}
"""

    response = llm.invoke(prompt)

    return {"messages":[response]}