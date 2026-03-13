from dataclasses import dataclass
from typing import Any, Dict, Tuple


@dataclass
class Thought:
    """A reasoning step taken by the agent."""

    text: str


@dataclass
class Action:
    """An action the agent wants to perform."""

    name: str
    params: Dict[str, Any]


class CropAgent:
    """A simple ReAct-style agent that processes crop data and updates state."""

    def react(self, crop_data: Dict[str, Any], state: Dict[str, Any]) -> Tuple[Thought, Action]:
        """Analyze crop data and generate a Thought + Action for state updates."""

        thought_text = (
            "I'll analyze the crop data to generate an insight that can be stored in the workflow state."
        )
        thought = Thought(text=thought_text)

        # Simple heuristic insight based on provided crop data
        crop_type = crop_data.get("crop_type", "unknown")
        yield_estimate = crop_data.get("yield_estimate")
        location = crop_data.get("location", "unknown location")

        insight = f"Crop: {crop_type} at {location}. "
        if yield_estimate is not None:
            insight += f"Estimated yield is {yield_estimate}."
        else:
            insight += "Yield estimate not provided."

        # Update state with the latest crop insight
        state["last_crop_insight"] = insight

        action = Action(name="store_crop_insight", params={"insight": insight})

        return thought, action
