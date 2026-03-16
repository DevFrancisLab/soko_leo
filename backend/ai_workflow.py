import sys
import os
from typing import Any, Dict

# Add the parent directory to the Python path so we can import from ai
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ai.run_workflow import run_workflow_for_backend


def run_main_workflow(market_data: str, weather_data: Dict[str, Any], crop_data: Dict[str, Any]) -> Dict[str, Any]:
    return run_workflow_for_backend(market_data, weather_data, crop_data)
