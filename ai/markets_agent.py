# markets_agent.py
from dotenv import load_dotenv
import os
import json
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from tools.tavily_tool import search_tool

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# --- Persistent Memory ---
MEMORY_FILE = os.path.join(os.path.dirname(__file__), "conversation_memory.json")

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
            messages = []
            for item in data:
                if item["role"] == "HumanMessage":
                    messages.append(HumanMessage(content=item["content"]))
                elif item["role"] == "AIMessage":
                    messages.append(AIMessage(content=item["content"]))
            return messages
    return []

def save_memory(messages):
    with open(MEMORY_FILE, "w") as f:
        json.dump([{"role": m.__class__.__name__, "content": m.content} for m in messages], f, indent=2)

conversation_history = load_memory()

# --- State definition ---
from typing import TypedDict, Annotated
class State(TypedDict):
    messages: Annotated[list, add_messages]
    location: str
    season: str

# --- System Prompt ---
SOKOLEO_SYSTEM_PROMPT = """
You are SokoLeo AI, an expert agricultural advisor specializing in helping Kenyan farmers maximize profits and efficiency.

CORE PRINCIPLES:
- Always prioritize farmer income and business sustainability
- Focus on practical, actionable advice over generic suggestions
- Base recommendations on current market trends, weather patterns, and logistics realities
- Emphasize high-demand crops, optimal pricing strategies, and efficient farming practices

EXPERTISE AREAS:
1. MARKET INTELLIGENCE: Current crop prices, demand trends in Nairobi/Mombasa markets, profitable varieties
2. WEATHER-ADAPTED FARMING: Seasonal planning, drought-resistant crops, rainfall timing
3. LOGISTICS & TRANSPORT: Cost-effective transport routes, storage solutions, market access
4. PROFIT OPTIMIZATION: Crop selection for margins, timing harvests, diversification strategies

RESPONSE GUIDELINES:
- Be specific: Name exact crops, prices, locations, and timeframes
- Provide numbers: Profit margins, costs, yields, market prices when possible
- Give actionable steps: "Plant X acres of Y crop by Z date" not "Consider planting"
- Consider farmer constraints: Small-scale operations, limited resources, local conditions
- Include risk mitigation: Weather contingencies, market fluctuations, alternative crops

AVOID:
- Vague advice like "good luck" or "keep trying"
- Unsubstantiated claims without data
- Overly technical jargon without explanation
- Generic farming platitudes

Your goal: Turn farming questions into profitable farming decisions.
"""
def extract_crop_recommendations(market_data: str) -> list:
    """
    Extract crop recommendations from market data string.
    
    Args:
        market_data: String containing market information
        
    Returns:
        List of unique crops found (case-insensitive, duplicates removed)
    """
    predefined_crops = [
        "maize",
        "beans",
        "tomatoes",
        "onions",
        "cabbage",
        "potatoes",
        "avocado",
        "bananas",
        "okra",
        "kale",
        "kales",
        "macadamia",
    ]

    # Scan the provided market data without concatenating raw titles + content.
    # The goal is to detect mentions of key crops without returning or exposing
    # the underlying search result text.
    data_lower_parts = []
    if isinstance(market_data, dict):
        results = market_data.get("results")
        if isinstance(results, list):
            for item in results:
                if not isinstance(item, dict):
                    continue
                title = str(item.get("title", ""))
                content = str(item.get("content", ""))
                if title:
                    data_lower_parts.append(title.lower())
                if content:
                    data_lower_parts.append(content.lower())
    elif isinstance(market_data, list):
        for item in market_data:
            data_lower_parts.append(str(item).lower())
    else:
        data_lower_parts.append(str(market_data).lower())

    data_lower = "\n".join(data_lower_parts)

    found = []
    for crop in predefined_crops:
        if crop in data_lower:
            found.append(crop.capitalize())

    # Preserve order and remove duplicates
    return list(dict.fromkeys(found))


def normalize_question(text: str) -> str:
    """Normalize user text to improve intent detection.

    This collapses repeated letters (common typos like "seell"), removes
    punctuation, and collapses whitespace.
    """

    import re

    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def contains_keyword(text: str, keywords: list[str]) -> bool:
    """Return True if any keyword is in the text, with fuzzy matching for typos."""

    import difflib
    import re

    text_lower = text.lower()
    # Direct substring match
    for kw in keywords:
        if kw in text_lower:
            return True

    # Token-level fuzzy match (handles typos like "seell")
    tokens = re.findall(r"\w+", text_lower)
    for token in tokens:
        matches = difflib.get_close_matches(token, keywords, n=1, cutoff=0.75)
        if matches:
            return True
    return False
def MarketPricesAgent(state: State):
    query = "current high demand crops in Kenya, market prices, profitable crops Nairobi Mombasa trends"
    data = search_tool.run(query)

    # Tavily returns a dict with a "results" list of search items
    results = data.get("results") if isinstance(data, dict) else None
    if not results:
        return "Market Prices: No market data returned."

    # Collect raw texts for analysis, but do not concatenate them for output.
    texts = []
    for item in results[:3]:
        if not isinstance(item, dict):
            continue
        title = str(item.get("title", ""))
        content = str(item.get("content", ""))
        if title:
            texts.append(title)
        if content:
            texts.append(content)

    if not texts:
        return "No usable market insights were returned from the market data source."

    lower_texts = [t.lower() for t in texts]

    # Identify high-demand crops and locations
    crops = extract_crop_recommendations({"results": results})
    locations = []
    for city in ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret"]:
        if any(city.lower() in t for t in lower_texts):
            locations.append(city)

    # Determine price trend sentiment
    # Determine price trend sentiment based on signals across sources
    rising_words = ["rising", "surge", "spike", "increasing", "up", "higher"]
    stable_words = ["stable", "steady", "unchanged", "flat"]
    falling_words = ["falling", "fall", "drop", "down", "decreasing", "slump"]

    def any_in_text(words: list[str]) -> bool:
        return any(w in t for t in lower_texts for w in words)

    if any_in_text(rising_words):
        trend = "rising"
    elif any_in_text(stable_words):
        trend = "stable"
    elif any_in_text(falling_words):
        trend = "falling"
    else:
        trend = "mixed"

    # Identify demand drivers
    drivers = []
    if any("high demand" in t or "demand" in t for t in lower_texts):
        drivers.append("strong demand")
    if any("shortage" in t or "limited" in t or "tight supply" in t for t in lower_texts):
        drivers.append("limited supply")
    if any("export" in t for t in lower_texts):
        drivers.append("export demand")
    if any("weather" in t or "drought" in t or "rain" in t for t in lower_texts):
        drivers.append("weather-driven supply changes")

    driver_phrase = ""
    if drivers:
        driver_phrase = " due to " + " and ".join(drivers)

    # Build a concise, expert-style paragraph
    market_place = (
        f"in markets such as {', '.join(locations)}" if locations else "in Kenyan urban markets"
    )

    if crops:
        crop_list = ", ".join(crops[:-1]) + (" and " + crops[-1] if len(crops) > 1 else crops[0])
        verb = "are" if len(crops) > 1 else "is"
        trend_phrase = {
            "rising": "rising",
            "stable": "steady",
            "falling": "falling",
            "mixed": "moving with demand",
        }[trend]
        return (
            f"Based on current market trends, {crop_list} {verb} currently in high demand {market_place}. "
            f"Prices are {trend_phrase}{driver_phrase}."
        )

    # Fallback when no specific crops could be extracted
    trend_phrase = {
        "rising": "are rising",
        "stable": "are steady",
        "falling": "are falling",
        "mixed": "are moving with demand",
    }[trend]
    return (
        f"Based on current market reports, prices {trend_phrase} {market_place}{driver_phrase}."
    )

def LogisticsAgent(state: State):
    return (
        "Logistics & Transport:\n"
        "- Use major highways and reliable routes for transport.\n"
        "- Store grains in cool, dry storage to prevent losses.\n"
        "- Optimize truckloads and plan delivery times to reduce costs."
    )

def WeatherAgent(state: State):
    return (
        "Weather & Crop Planning:\n"
        "- Monitor rainfall and temperature forecasts.\n"
        "- Plant drought-resistant crops if rains are low.\n"
        "- Harvest early if rains are delayed or unpredictable."
    )

def ProfitAgent(state: State):
    return (
        "Profit & Crop Selection:\n"
        "- Plant crops with high local demand and margin.\n"
        "- Consider crop rotation to maintain soil fertility.\n"
        "- Diversify crops to reduce market risks."
    )

def CropRecommendationAgent(state: State, market_data: str):
    last_question = state["messages"][-1].content
    normalized_question = normalize_question(last_question)
    recommendations = []

    # Determine intent from user question (order matters)
    if contains_keyword(normalized_question, ["transport", "route", "truck", "logistics"]):
        intent = "transport"
    elif contains_keyword(normalized_question, ["weather", "rain", "temperature", "forecast"]):
        intent = "weather"
    elif contains_keyword(normalized_question, ["plant"]):
        intent = "plant"
    elif contains_keyword(normalized_question, ["sell", "market", "where", "price", "demand", "profit"]):
        intent = "sell"
    else:
        intent = None

    # Detect location from question for context-aware recommendations
    location = None
    for loc in ["Makueni", "Nairobi", "Kisumu"]:
        if loc.lower() in normalized_question:
            location = loc
            break

    # Extract crops from market_data and bias recommendations toward location-suitable crops
    crops = extract_crop_recommendations(market_data) if market_data else []

    # Location-based crop preference (for planting recommendations)
    location_crops = {
        "Makueni": ["Sorghum", "Millet", "Green grams", "Mangoes"],
        "Nairobi": ["Onions", "Tomatoes", "Okra", "Cabbage"],
        "Kisumu": ["Rice", "Sugarcane", "Vegetables"],
    }

    if location and location in location_crops:
        preferred = [c for c in location_crops[location] if c not in crops]
        crops = preferred + crops
    # Respond based on detected intent
    if intent == "plant":
        if location:
            if location == "Makueni":
                recommendations.append(
                    "For your situation in Makueni, drought-resistant crops like sorghum, millet, green grams, and mangoes tend to perform best because rainfall is limited and these crops hold value even in dry seasons."
                )
            elif location == "Nairobi":
                recommendations.append(
                    "For Nairobi, focus on high-demand vegetables like onions and tomatoes that sell quickly in urban markets and often command higher prices because of daily consumer demand."
                )
            elif location == "Kisumu":
                recommendations.append(
                    "For Kisumu’s humid climate, rice, sugarcane, and vegetables thrive; these crops benefit from year-round moisture and meet steady local demand."
                )

        if crops:
            # Provide reasoning for each recommended crop
            crop_reasons = {
                "Onions": "consistent demand in urban markets and generally strong prices",
                "Okra": "high demand in both local and export markets with good margins",
                "Tomatoes": "steady demand and multiple harvest cycles per season",
                "Maize": "staple food demand is stable and prices tend to hold",
                "Beans": "strong domestic demand and good storage life for selling later",
                "Avocado": "export demand keeps prices high, especially in dry seasons",
                "Cabbage": "popular in urban markets and has a quick harvest turnaround",
                "Potatoes": "widely consumed with consistent demand and good yield per acre",
                "Bananas": "year-round demand and good returns in local markets",
                "Sorghum": "drought tolerant and in demand where rainfall is low",
                "Millet": "resilient in dry conditions and valued in local diets",
                "Green grams": "fast-maturing and profitable in drier zones",
                "Macadamia": "high export value when mature, suitable for investment crops",
            }

            for crop in crops:
                reason = crop_reasons.get(crop, "strong local demand and good margins")
                recommendations.append(
                    f"{crop} is profitable because it has {reason}."
                )
        else:
            recommendations.append(
                "Planting recommendation: Consider maize, beans, or tomatoes based on local demand, as these crops generally have stable prices and good buyer interest."
            )

        recommendations.append("- Rotate crops and test soil to keep yields high.")

    elif intent == "sell":
        question_crops = extract_crop_recommendations(last_question)
        preferred_crop = question_crops[0] if question_crops else None

        # Detect whether the user is asking what to sell vs where to sell
        wants_what = contains_keyword(last_question, ["what"]) and contains_keyword(last_question, ["sell"])
        wants_where = contains_keyword(last_question, ["where"]) and contains_keyword(last_question, ["sell"])

        # Common market destinations (fall back for general advice)
        all_markets = {
            "default": "Wakulima Market in Nairobi",
            "tomatoes": "Wakulima Market in Nairobi",
            "onions": "Gikomba Market in Nairobi",
            "okra": "Kongowea Market in Mombasa",
            "kale": "Wakulima Market in Nairobi",
            "rice": "Kibuye Market in Kisumu",
        }

        def choose_market(crop: str | None) -> str:
            if not crop:
                return all_markets["default"]
            return all_markets.get(crop.lower(), all_markets["default"])

        # When the user asks what to sell, provide a crop recommendation and where to sell it
        if wants_what:
            if preferred_crop:
                market = choose_market(preferred_crop)
                recommendations.append(
                    f"Based on current market demand, you can sell {preferred_crop.lower()} at {market}, where buyers pay more for consistent quality."
                )
            else:
                recommendations.append(
                    "For good turnover, sell tomatoes or onions in Nairobi markets, where daily demand keeps prices steady and buyers are ready."
                )

            # Add a quick selling tip for the crop(s)
            tip_crop = preferred_crop.lower() if preferred_crop else "these crops"
            recommendations.append(
                f"Quick tip: {tip_crop.capitalize()} sell fastest when brought early in the morning, and buyers pay more for produce that is clean and well sorted."
            )

        # When the user asks where to sell, focus on market locations and practicality
        if wants_where:
            crop_for_market = preferred_crop or (crops[0] if crops else None)
            market = choose_market(crop_for_market)
            if crop_for_market:
                recommendations.append(
                    f"For {crop_for_market.lower()}, a top option is {market} because it draws large wholesale buyers who pay premiums for consistent supply."
                )
            else:
                recommendations.append(
                    f"A reliable option is {market}, as it serves many traders and moves large volumes of vegetables and staples daily."
                )

            recommendations.append(
                "Tip: Deliver early (6–8am) and keep produce well packed; buyers pay more for fresh, clean stock."
            )

    elif intent == "transport":
        recommendations.append("Transport advice:")
        recommendations.append("- Use major highways and reliable routes to reduce delays.")
        recommendations.append("- Plan shipments early in the day to avoid traffic and spoilage.")

    elif intent == "weather":
        recommendations.append("Weather advice:")
        recommendations.append("- Plant after the next expected rain window to ensure good germination.")
        recommendations.append("- Use early-maturing varieties if dry spells are forecast.")

    else:
        recommendations.append("I can provide specific advice for planting, selling, transport, or weather. Please clarify which you need.")

    return "\n".join(recommendations)

# --- Dynamic Routing with Merged Output ---
def route_agent(state: State):
    question = state["messages"][-1].content
    normalized_question = normalize_question(question)
    outputs = []
    market_data = ""

    # Determine intent (order matters to avoid keyword overlap)
    if contains_keyword(normalized_question, ["transport", "route", "truck", "logistics"]):
        intent = "transport"
    elif contains_keyword(normalized_question, ["weather", "rain", "temperature", "forecast"]):
        intent = "weather"
    elif contains_keyword(normalized_question, ["plant"]):
        intent = "plant"
    elif contains_keyword(normalized_question, ["sell", "market", "where", "price", "demand", "profit"]):
        intent = "sell"
    else:
        intent = None

    # Execute based on intent (avoid irrelevant output)
    if intent == "plant":
        print(f"[DEBUG] Intent=plant, fetching market data for question: {question}")
        market_data = MarketPricesAgent(state)
        outputs.append(market_data)
        outputs.append(CropRecommendationAgent(state, market_data))

    elif intent == "sell":
        print(f"[DEBUG] Intent=sell, fetching market data for question: {question}")
        market_data = MarketPricesAgent(state)
        outputs.append(market_data)
        outputs.append(CropRecommendationAgent(state, market_data))

    elif intent == "transport":
        print("[DEBUG] Intent=transport, triggering LogisticsAgent")
        outputs.append(LogisticsAgent(state))

    elif intent == "weather":
        print("[DEBUG] Intent=weather, triggering WeatherAgent")
        outputs.append(WeatherAgent(state))

    else:
        outputs.append("I can help with planting advice, selling locations, transport logistics, or weather planning. What would you like?")

    # Merge all agent outputs into a single answer
    merged_answer = "\n\n".join(outputs)
    return {"messages": [AIMessage(content=merged_answer)]}

# --- Build StateGraph ---
builder = StateGraph(State)
builder.add_node("dynamic_router", route_agent)
builder.add_edge(START, "dynamic_router")
builder.add_edge("dynamic_router", END)

graph = builder.compile(checkpointer=MemorySaver())

# --- Interactive Loop ---
print("\n🌽 SokoLeo AI Market System with Merged Multi-Agent Output")
print("Type 'exit' to quit.\n")

while True:
    question = input("Farmer: ")
    if question.lower() == "exit":
        break

    state = {
        "messages": [HumanMessage(content=question)],
        "location": "Kenya",
        "season": "current"
    }

    response = graph.invoke(state, config={"configurable": {"thread_id": "farmer_session"}})
    answer = response["messages"][-1].content

    print("\nSokoLeo:\n")
    print(answer)
    print()

    # Update memory
    conversation_history.append(HumanMessage(content=question))
    conversation_history.append(AIMessage(content=answer))
    save_memory(conversation_history)