import json
import os
from datetime import datetime

MEMORY_FILE = "state/market_memory.json"

# Ensure the file exists
if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump({}, f)

def save_price(crop: str, market: str, price: float):
    with open(MEMORY_FILE, "r") as f:
        data = json.load(f)

    if crop not in data:
        data[crop] = {}

    if market not in data[crop]:
        data[crop][market] = []

    # Append price with timestamp
    data[crop][market].append({"price": price, "timestamp": datetime.now().isoformat()})

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_prices(crop: str, market: str):
    with open(MEMORY_FILE, "r") as f:
        data = json.load(f)

    return data.get(crop, {}).get(market, [])

def get_trend(crop: str, market: str):
    prices = get_prices(crop, market)
    if len(prices) < 2:
        return "Not enough data to detect trend"

    last = prices[-1]["price"]
    prev = prices[-2]["price"]

    if last > prev:
        return "Price is increasing 📈"
    elif last < prev:
        return "Price is decreasing 📉"
    else:
        return "Price is stable ➖"