# =========================
# SokoLeo Market Agent
# =========================

from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages

from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.memory import MemorySaver

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.tools.tavily_search import TavilySearchResults

from dotenv import load_dotenv
import os


# =========================
# Load Environment Variables
# =========================

load_dotenv()


# =========================
# Memory
# =========================

memory = MemorySaver()


# =========================
# Graph State
# =========================

class State(TypedDict):
    messages: Annotated[list, add_messages]


# =========================
# Initialize LLM
# =========================

llm = init_chat_model(
    "groq:llama-3.3-70b-versatile"
)


# =========================
# Tavily Search Tool
# =========================

search_tool = TavilySearchResults(
    max_results=3
)

tools = [search_tool]


# =========================
# Bind Tools
# =========================

llm_with_tools = llm.bind_tools(tools)


# =========================
# System Prompt
# =========================

system_prompt = SystemMessage(
    content="""
You are SokoLeo, an AI agricultural market assistant for Kenyan farmers.

Your job is to provide:
- current crop prices
- agricultural news
- market demand insights
- selling advice for farmers

Focus on Kenya markets.

When answering:
1. Give the latest market data
2. Explain what it means
3. Give a short recommendation to farmers
"""
)


# =========================
# LLM Node
# =========================

def tool_calling_llm(state: State):

    messages = state["messages"]

    response = llm_with_tools.invoke(
        [system_prompt] + messages
    )

    return {"messages": [response]}


# =========================
# Build Graph
# =========================

builder = StateGraph(State)

builder.add_node("tool_calling_llm", tool_calling_llm)

builder.add_node("tools", ToolNode(tools))


# =========================
# Graph Flow
# =========================

builder.add_edge(START, "tool_calling_llm")

builder.add_conditional_edges(
    "tool_calling_llm",
    tools_condition
)

builder.add_edge("tools", "tool_calling_llm")


# =========================
# Compile Graph
# =========================

graph = builder.compile(checkpointer=memory)


# =========================
# Runtime Config
# =========================

config = {
    "configurable": {
        "thread_id": "1"
    }
}


# =========================
# Run Query
# =========================

response = graph.invoke(
    {
        "messages": [
            HumanMessage(content="What is the current maize price in Kenya?")
        ]
    },
    config=config
)


# =========================
# Interactive Chat Loop
# =========================

print("\n🌽 SokoLeo Market Agent")
print("Type 'exit' to quit\n")

while True:

    user_input = input("Farmer: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye 👋")
        break

    response = graph.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ]
        },
        config=config
    )

    print("\nSokoLeo:\n")
    print(response["messages"][-1].content)
    print("\n")