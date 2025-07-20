# orchestrator.py

import json
import logging
from pathlib import Path
from smart_travel_concierge.agents.memory_agent import store_memory, get_memory
from smart_travel_concierge.agents.planner_agent import PlannerAgent
from smart_travel_concierge.agents.flight_agent import get_mock_flights
from smart_travel_concierge.agents.food_agent import run_food_agent



# --- Configure logging ---
logging.basicConfig(filename='orchestrator.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# --- Base path for agent spec files ---
BASE_PATH = "smart_travel_concierge/specs"

# --- Simulated agent logic (reads from spec output files) ---
def run_planner_agent(task_state):
    user_goal = task_state.get("user_goal", "")
    agent = PlannerAgent(user_goal)
    result = agent.get_output()

    # Update task_state with structured info from PlannerAgent
    task_state["memory"]["PlannerAgent"] = result["output"]
    task_state["subtasks"] = result["output"]["subtasks"]
    task_state["location"] = result["output"]["location"]
    task_state["dates"] = result["output"]["dates"]
    task_state["travelers"] = result["output"]["travelers"]
    task_state["budget"] = result["output"]["budget"]

    return result["output"]

def run_flight_agent(task_state):
    planner_output = task_state["memory"].get("PlannerAgent", {})
    origin = "JFK"  # You can later make this dynamic
    destination = "JED"
    dates = planner_output.get("dates", {})
    return get_mock_flights(origin, destination, dates.get("start"), dates.get("end"))

def run_memory_agent(task_state):
    store_memory("preferred_airline", "Saudia")
    store_memory("preferred_food", "halal")
    store_memory("budget_level", "low")
    
    return {
        "stored_keys": ["preferred_airline", "preferred_food", "budget_level"]
    }


from smart_travel_concierge.agents.hotel_agent import get_mock_hotels

def run_hotel_agent(task_state):
    context = task_state["memory"].get("PlannerAgent", {})
    location = context.get("location", "Makkah")
    dates = context.get("dates", {})
    budget = context.get("budget", {}).get("level", "low")

    checkin = dates.get("start", "2025-12-10")
    checkout = dates.get("end", "2025-12-15")

    return get_mock_hotels(location, checkin, checkout, budget)


def run_food_agent(task_state):
    with open(f"{BASE_PATH}/food_spec.json") as f:
        return json.load(f)["output"]
    
def run_itinerary_agent(task_state):
    with open(f"{BASE_PATH}/itinerary_spec.json") as f:
        return json.load(f)["output"]


# --- Map agent names to functions ---
AGENT_FUNCTIONS = {
    "PlannerAgent": run_planner_agent,
    "FlightAgent": run_flight_agent,
    "HotelAgent": run_hotel_agent,
    "FoodAgent": run_food_agent,
    "ItineraryAgent": run_itinerary_agent,
    "MemoryAgent": run_memory_agent
}

AGENT_SEQUENCE = list(AGENT_FUNCTIONS.keys())

# --- Run single agent step ---
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

            # Validate output format
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


# --- Move to next agent ---
def advance_agent(task_state):
    try:
        idx = AGENT_SEQUENCE.index(task_state["current_agent"])
        task_state["current_agent"] = (
            AGENT_SEQUENCE[idx + 1] if idx + 1 < len(AGENT_SEQUENCE) else None
        )
    except ValueError:
        task_state["current_agent"] = None
    return task_state


# --- Main orchestrator run ---
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
