from langchain.chat_models import init_chat_model
import os

# Set Vertex AI API key
os.environ["GOOGLE_API_KEY"] = os.getenv("VERTEX_AI_API_KEY")

llm = init_chat_model("google_genai:gemini-1.5-pro")

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