# test_memory_agent.py

from smart_travel_concierge.agents.memory_agent import store_memory, get_memory, clear_memory

def test_memory():
    clear_memory()

    print("➡️ Storing preferences...")
    store_memory("preferred_airline", "Saudia")
    store_memory("preferred_food", "halal")
    store_memory("budget_level", "low")

    print("\n✅ Retrieving stored values:")
    print("preferred_airline:", get_memory("preferred_airline"))  # should be Saudia
    print("preferred_food:", get_memory("preferred_food"))        # should be halal
    print("budget_level:", get_memory("budget_level"))            # should be low
    print("favorite_color:", get_memory("favorite_color"))        # should be None

if __name__ == "__main__":
    test_memory()
