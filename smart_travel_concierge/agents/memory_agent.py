# smart-travel-concierge/agents/memory_agent.py

import json
from pathlib import Path

# Memory file location (relative to project root)
MEMORY_FILE = Path("smart_travel_concierge/memory_store.json")

# Load memory from file
def load_memory():
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

# Save memory to file
def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

# Store a key-value pair
def store_memory(key, value):
    memory = load_memory()
    memory[key] = value
    save_memory(memory)

# Retrieve a value for a given key
def get_memory(key):
    memory = load_memory()
    return memory.get(key, None)

# Clear all memory
def clear_memory():
    if MEMORY_FILE.exists():
        MEMORY_FILE.unlink()
