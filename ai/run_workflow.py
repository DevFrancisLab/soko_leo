import yaml
from typing import Any, Dict

from ai.agents import CropAgent, WeatherAgent, MarketAgent


AGENT_CLASSES = {
    "MarketAgent": MarketAgent,
    "WeatherAgent": WeatherAgent,
    "CropAgent": CropAgent,
}


def run_workflow(workflow_path: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Load a workflow YAML and run its nodes in order, returning the final state."""

    with open(workflow_path, "r") as f:
        workflow = yaml.safe_load(f)

    # Initialize state based on inputs
    state: Dict[str, Any] = {**inputs}

    # Instantiate agent objects for each node
    nodes = workflow.get("nodes", [])
    agents = {}
    for node in nodes:
        agent_name = node["agent"]
        agent_cls = AGENT_CLASSES.get(agent_name)
        if not agent_cls:
            raise ValueError(f"Unknown agent: {agent_name}")
        agents[node["id"]] = agent_cls()

    # Run nodes in order they are defined (simple workflow execution)
    for node in nodes:
        node_id = node["id"]
        agent = agents[node_id]

        # Gather inputs for this node
        node_inputs = {}
        for inp in node.get("inputs", []):
            if inp in state:
                node_inputs[inp] = state[inp]
            else:
                node_inputs[inp] = None

        # Call react: (thought, action) = agent.react(input1, input2, ..., state)
        # We pass both the raw inputs dict and shared state for flexibility.
        thought, action = agent.react(node_inputs, state)

        # Store action output(s) in state
        for output in node.get("outputs", []):
            state[output] = action.params.get(output, action.params)

        # Also keep last thought for debugging
        state[f"{node_id}_thought"] = thought.text

    return state


if __name__ == "__main__":
    sample_inputs = {
        "market_data": "Prices are rising due to supply constraints.",
        "weather_data": {"temp": 25, "condition": "sunny"},
        "crop_data": {"crop_type": "maize", "yield_estimate": "high", "location": "Nairobi"},
    }

    result = run_workflow("ai/workflow.yaml", sample_inputs)
    print("Workflow result:\n", result)
