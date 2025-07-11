# orchestrator.py

import json
import logging
from pathlib import Path

# --- Configure logging ---
logging.basicConfig(filename='orchestrator.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# --- Simulated agent logic (replace with actual API calls later) ---
def run_planner_agent(task_state):
    with open("planner_spec.json") as f:
        return json.load(f)["output"]

def run_flight_agent(task_state):
    with open("flight_spec.json") as f:
        return json.load(f)["output"]

def run_hotel_agent(task_state):
    with open("hotel_spec.json") as f:
        return json.load(f)["output"]

def run_food_agent(task_state):
    with open("food_spec.json") as f:
        return json.load(f)["output"]

def run_itinerary_agent(task_state):
    with open("itinerary_spec.json") as f:
        return json.load(f)["output"]

AGENT_FUNCTIONS = {
    "PlannerAgent": run_planner_agent,
    "FlightAgent": run_flight_agent,
    "HotelAgent": run_hotel_agent,
    "FoodAgent": run_food_agent,
    "ItineraryAgent": run_itinerary_agent
}

AGENT_SEQUENCE = list(AGENT_FUNCTIONS.keys())

# --- Agent Runner ---
def run_agent_step(task_state, retries=2):
    current_agent = task_state["current_agent"]
    logging.info(f"🧠 Running {current_agent}")

    agent_fn = AGENT_FUNCTIONS.get(current_agent)
    if not agent_fn:
        logging.warning(f"No function defined for {current_agent}")
        return advance_agent(task_state)

    for attempt in range(1, retries + 2):
        try:
            output = agent_fn(task_state)

            # Validate expected keys (very basic validation)
            if not isinstance(output, dict):
                raise ValueError("Agent output must be a dictionary.")

            task_state["memory"][current_agent] = output
            logging.info(f"✅ {current_agent} success on attempt {attempt}")
            break

        except Exception as e:
            logging.error(f"❌ {current_agent} failed on attempt {attempt}: {e}")
            if attempt == retries + 1:
                print(f"‼️ {current_agent} failed after {retries + 1} attempts. Skipping...")
                task_state["memory"][current_agent] = {"error": str(e)}

    return advance_agent(task_state)


def advance_agent(task_state):
    try:
        idx = AGENT_SEQUENCE.index(task_state["current_agent"])
        task_state["current_agent"] = (
            AGENT_SEQUENCE[idx + 1] if idx + 1 < len(AGENT_SEQUENCE) else None
        )
    except ValueError:
        task_state["current_agent"] = None
    return task_state


def main():
    try:
        with open("mcp_task.json") as f:
            task_state = json.load(f)
    except Exception as e:
        logging.critical(f"❌ Failed to load task state: {e}")
        print("❌ Could not load initial MCP task.")
        return

    print("🚀 Starting MCP Orchestration...\n")
    logging.info("🚀 MCP orchestration started.")

    while task_state["current_agent"]:
        print(f"🔁 Executing {task_state['current_agent']}")
        task_state = run_agent_step(task_state)

    print("🎉 All agents executed.")
    logging.info("🎉 All agents executed successfully.")

    print("🗂 Final shared memory:")
    print(json.dumps(task_state["memory"], indent=2))

    with open("mcp_result.json", "w") as f:
        json.dump(task_state, f, indent=2)
        logging.info("✅ Final task state written to mcp_result.json")


if __name__ == "__main__":
    main()
