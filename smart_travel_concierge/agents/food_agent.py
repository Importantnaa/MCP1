# smart_travel_concierge/agents/food_agent.py
import json
import os

def run_food_agent(task_state):
    base_path = os.path.dirname(__file__)
    spec_path = os.path.join(base_path, "../specs/food_spec.json")

    with open(spec_path) as f:
        data = json.load(f)

    dietary_prefs = task_state.get("dietary_preferences", ["halal"])

    filtered = [
        r for r in data["output"]["restaurants"]
        if any(pref.lower() in r.get("type", "").lower() for pref in dietary_prefs)
    ]

    return {
        "restaurants": filtered[:3]
    }
