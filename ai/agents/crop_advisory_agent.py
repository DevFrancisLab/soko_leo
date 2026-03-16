from langchain.chat_models import init_chat_model

llm = init_chat_model("groq:llama-3.3-70b-versatile")

def crop_advisory_agent(state):

    question = state["messages"][-1].content

    prompt = f"""
You are an agricultural advisor for Kenyan farmers.

Question:
{question}

Provide clear advice.
"""

    response = llm.invoke(prompt)

    return {"messages":[response]}