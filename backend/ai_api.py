from fastapi import FastAPI
from pydantic import BaseModel

from ai.run_workflow import run_workflow


class InsightRequest(BaseModel):
    market_data: str
    weather_data: dict
    crop_data: dict


class InsightResponse(BaseModel):
    result: dict


app = FastAPI()


@app.post("/api/ai/market-insight/", response_model=InsightResponse)
def market_insight(req: InsightRequest):
    inputs = {
        "market_data": req.market_data,
        "weather_data": req.weather_data,
        "crop_data": req.crop_data,
    }
    state = run_workflow("ai/workflow.yaml", inputs)
    return {"result": state}
