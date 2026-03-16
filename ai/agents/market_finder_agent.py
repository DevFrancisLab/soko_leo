from tools.tavily_tool import search_tool
from langchain.chat_models import init_chat_model

llm = init_chat_model("groq:llama-3.3-70b-versatile")

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