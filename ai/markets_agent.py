# markets_agent.py

import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_tavily import TavilySearch
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()  # Load environment variables from .env

# Ensure TAVILY_API_KEY is set
tavily_api_key = os.getenv("TAVILY_API_KEY")
if not tavily_api_key:
    raise ValueError("TAVILY_API_KEY is not set in your environment variables.")

# Initialize Tavily search tool
search_tool = TavilySearch(
    tavily_api_key=tavily_api_key,
    max_results=3
)

# Initialize LLM
llm = init_chat_model("groq:llama-3.3-70b-versatile")

# Initialize memory saver
memory = MemorySaver()

print("\n🌽 SokoLeo AI Market System with Memory")
print("Type 'exit' to quit.\n")

# Store conversation history
conversation_history = []

def ask_sokoleo(question: str) -> str:
    """
    Processes farmer's question using TavilySearch and LLM reasoning.
    Maintains memory of previous questions to give progressive advice.
    """
    # Step 1: Fetch relevant market info
    try:
        results = search_tool.invoke(f"{question} Kenya agriculture market")
    except Exception as e:
        return f"Sorry, I couldn't fetch market info due to an error: {e}"

    # Step 2: Convert results into a text summary
    if isinstance(results, list):
        summary_parts = []
        for r in results:
            snippet = r.get("snippet") or r.get("title") or ""
            summary_parts.append(snippet)
        market_summary = "\n".join(summary_parts)
    else:
        market_summary = str(results)

    # Step 3: Prepare conversation context
    context_messages = []
    for msg in conversation_history:
        context_messages.append(msg)
    context_messages.append(HumanMessage(content=question))

    # Step 4: Build prompt with market info
    prompt = f"""
You are an expert agricultural market advisor in Kenya. 
Use the market info below to answer the farmer's question in a practical, profit-oriented way.
Include actionable recommendations on:
- What crops to plant for profit
- Where to sell crops and to whom
- Storage and transportation best practices
- Timing based on weather and market demand

Farmer's question: {question}

Market info:\n{market_summary}
"""

    # Step 5: Generate AI response
    try:
        response = llm.invoke(context_messages + [HumanMessage(content=prompt)])
        answer = response.content
    except Exception as e:
        answer = f"Sorry, I couldn't generate advice due to an error: {e}"

    # Step 6: Save in conversation history for memory
    conversation_history.append(HumanMessage(content=question))
    conversation_history.append(AIMessage(content=answer))
    memory.save(conversation_history)  # optional persistent memory

    return answer


# Main loop
while True:
    question = input("Farmer: ").strip()
    if not question:
        continue

    if question.lower() == "exit":
        print("Exiting SokoLeo. Happy farming! 🌽")
        break

    answer = ask_sokoleo(question)
    print("\nSokoLeo:\n")
    print(answer)
    print("\n" + "-"*60 + "\n")