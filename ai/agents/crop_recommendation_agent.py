# agents/crop_recommendation_agent.py
from langchain_core.messages import AIMessage

def CropRecommendationAgent(state: dict):
    """
    Combines inputs from Market, Weather, and Profit agents
    to recommend which crops to plant and when.
    """

    last_question = state["messages"][-1].content
    location = state.get("location", "Kenya")
    season = state.get("season", "current")

    # Basic dynamic logic for demo
    # In production, you can query Tavily for real-time prices and demand
    recommendations = []

    if "profit" in last_question.lower() or "plant" in last_question.lower():
        recommendations.append(
            f"- Plant high-demand crops like maize, beans, or tomatoes in {location} "
            f"this {season} season for maximum profit."
        )

    if "weather" in last_question.lower() or "rain" in last_question.lower():
        recommendations.append(
            "- Check rainfall forecasts: plant drought-resistant crops if rains are low."
        )

    if not recommendations:
        recommendations.append(
            "- Diversify crops and monitor local markets and weather patterns."
        )

    advice_text = "Crop Recommendation Agent Advice:\n" + "\n".join(recommendations)

    return {"messages": [AIMessage(content=advice_text)]}