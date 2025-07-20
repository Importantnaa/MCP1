# app.py

import streamlit as st
import json
from pathlib import Path

# Load MCP results
RESULT_PATH = Path("mcp_result.json")
MEMORY_PATH = Path("smart_travel_concierge/memory_store.json")

def load_json(file_path):
    if file_path.exists():
        with open(file_path) as f:
            return json.load(f)
    return {}

def main():
    st.set_page_config(page_title="Smart Travel Concierge", layout="wide")
    st.title("🧳 Smart Travel Concierge")
    st.markdown("Plan your trip with AI-powered itinerary suggestions!")

    with st.sidebar:
        st.header("✈️ User Preferences")
        destination = st.text_input("Destination", "Makkah")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        budget = st.selectbox("Budget", ["low", "medium", "high"])
        dietary = st.multiselect("Dietary Preferences", ["halal", "vegetarian", "vegan"], default=["halal"])
        if st.button("Save Preferences"):
            memory = {
                "preferred_airline": "Saudia",
                "preferred_food": dietary[0] if dietary else "halal",
                "budget_level": budget
            }
            with open(MEMORY_PATH, "w") as f:
                json.dump(memory, f, indent=2)
            st.success("Preferences saved!")

    result = load_json(RESULT_PATH)
    memory = load_json(MEMORY_PATH)

    if result:
        st.subheader("📋 Trip Overview")
        st.json(result.get("memory", {}))

        st.subheader("🗓️ Daily Itinerary")
        itinerary = result.get("memory", {}).get("ItineraryAgent", {})
        for day, events in itinerary.items():
            with st.expander(day.capitalize()):
                for e in events:
                    st.markdown(f"- {e}")

        st.subheader("🍽️ Food Options")
        for r in result.get("memory", {}).get("FoodAgent", {}).get("restaurants", []):
            st.markdown(f"**{r['name']}** ({r['type']}) — {r['rating']} ⭐️ – {r['distance']}")

        st.subheader("🏨 Hotel Options")
        for h in result.get("memory", {}).get("HotelAgent", {}).get("hotels", []):
            st.markdown(f"**{h['name']}** – {h['price_per_night']}$ per night – {h['distance_to_kaaba']} – {h['rating']} ⭐️")

        st.subheader("🛫 Flights")
        for f in result.get("memory", {}).get("FlightAgent", {}).get("flights", []):
            st.markdown(f"**{f['airline']}** – ${f['price']} – Depart: {f['depart']} – Return: {f['return']}")

if __name__ == "__main__":
    main()
