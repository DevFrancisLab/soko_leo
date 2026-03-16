from tools.tavily_tool import search_tool
from langchain.chat_models import init_chat_model

llm = init_chat_model("groq:llama-3.3-70b-versatile")

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