import streamlit as st
import json
from pathlib import Path

# --- Paths to your orchestrator output and memory files ---
RESULT_PATH = Path("mcp_result.json")
MEMORY_PATH = Path("smart_travel_concierge/memory_store.json")

def load_json(file_path: Path):
    if file_path.exists():
        with open(file_path) as f:
            return json.load(f)
    return {}

# --- Streamlit page config and styling ---
st.set_page_config(page_title="Smart Travel Concierge", layout="wide", page_icon="🌍")
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        color: #ffffff;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stMarkdown h2 { 
        color: #ffd700; 
        font-size: 28px; 
    }
    .st-expanderHeader { 
        font-size: 18px; 
        color: #ffffff; 
    }
    .stTextInput input, 
    .stSelectbox div div input, 
    .stMultiSelect div div div {
        background-color: #252633; 
        color: white; 
        border-radius: 5px;
    }
    button[kind="primary"] {
        background-color: #ffd700; 
        color: #000; 
        border-radius: 25px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌍 Smart Travel Concierge — Premium Edition")
st.markdown("Plan your luxury journey with tailored recommendations and visual previews.")

# --- Sidebar: Collect user preferences ---
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

# --- Load output from your orchestrator ---
result = load_json(RESULT_PATH)

if result:
    memory = result.get("memory", {})

    # --- Create tabs ---
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Overview", "🛫 Flights", "🏨 Hotels", "🍽️ Food", "📅 Itinerary"
    ])

    # Tab 1: Trip Summary
    with tab1:
        st.subheader("📋 Trip Summary")
        st.json(memory.get("PlannerAgent", {}))

    # Tab 2: Flights
    with tab2:
        st.subheader("🛫 Flights")
        flights = memory.get("FlightAgent", {}).get("flights", [])
        for f in flights:
            st.markdown(
                f"**{f['airline']}** — ${f['price']} — "
                f"Depart: {f['depart']} — Return: {f['return']}"
            )

    # Tab 3: Hotels with images + maps link
    with tab3:
        st.subheader("🏨 Hotel Options")
        hotels = memory.get("HotelAgent", {}).get("hotels", [])
        # Static image URLs keyed by hotel name
        hotel_images = {
            "Hilton Makkah":    "https://images.unsplash.com/photo-1558959357-685f9c7ace7b",
            "Swissotel Makkah": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb",
            "Al Safwah Hotel":  "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b"
        }
        for h in hotels:
            img_url = hotel_images.get(h["name"], list(hotel_images.values())[0])
            maps_link = (
                "https://www.google.com/maps/search/?api=1&query="
                + h["name"].replace(" ", "+") + "+Makkah"
            )
            st.image(img_url, width=600, caption=h["name"])
            st.markdown(f"- **Price**: ${h['price_per_night']}")
            st.markdown(f"- **Distance to Kaaba**: {h['distance_to_kaaba']}")
            st.markdown(f"- **Rating**: {h['rating']} ⭐️")
            st.markdown(f"[🗺 View on Google Maps]({maps_link})")
            st.markdown("---")

    # Tab 4: Restaurants with images + maps link
    with tab4:
        st.subheader("🍽️ Restaurant Options")
        restaurants = memory.get("FoodAgent", {}).get("restaurants", [])
        # One static demo image for all halal food
        food_img = "https://images.unsplash.com/photo-1562967916-eb82221dfb44"
        for r in restaurants:
            maps_link = (
                "https://www.google.com/maps/search/?api=1&query="
                + r["name"].replace(" ", "+") + "+Makkah"
            )
            st.image(food_img, width=600, caption=r["name"])
            st.markdown(f"- **Type**: {r['type']}")
            st.markdown(f"- **Distance**: {r['distance']}")
            st.markdown(f"- **Rating**: {r['rating']} ⭐️")
            st.markdown(f"[🗺 View on Google Maps]({maps_link})")
            st.markdown("---")

    # Tab 5: Day-by-day Itinerary
    with tab5:
        st.subheader("📅 Daily Itinerary")
        itinerary = memory.get("ItineraryAgent", {})
        if itinerary:
            for day, events in itinerary.items():
                with st.expander(day.capitalize()):
                    for e in events:
                        st.markdown(f"- {e}")
        else:
            st.warning("Itinerary not available yet.")

else:
    st.info("🚀 Run your orchestrator first to generate trip data (mcp_result.json).")
