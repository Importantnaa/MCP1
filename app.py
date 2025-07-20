import streamlit as st
import json
from pathlib import Path

# --- Paths to orchestrator output and memory ---
RESULT_PATH = Path("mcp_result.json")
MEMORY_PATH = Path("smart_travel_concierge/memory_store.json")

def load_json(file_path: Path):
    if file_path.exists():
        with open(file_path) as f:
            return json.load(f)
    return {}

# --- Streamlit layout and style ---
st.set_page_config(page_title="Smart Travel Concierge", layout="wide", page_icon="🌍")
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        color: #ffffff;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stMarkdown h2 { color: #ffd700; font-size: 28px; }
    .st-expanderHeader { font-size: 18px; color: #ffffff; }
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

# --- Sidebar for preferences ---
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

# --- Load orchestrator result ---
result = load_json(RESULT_PATH)

if result:
    memory = result.get("memory", {})

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Overview", "🛫 Flights", "🏨 Hotels", "🍽️ Food", "📅 Itinerary"])

    # Tab 1: Planner Summary
    with tab1:
        st.subheader("📋 Trip Summary")
        st.json(memory.get("PlannerAgent", {}))

    # Tab 2: Flights
    with tab2:
        st.subheader("🛫 Flights")
        flights = memory.get("FlightAgent", {}).get("flights", [])
        for f in flights:
            st.markdown(f"**{f['airline']}** — ${f['price']} — Depart: {f['depart']} — Return: {f['return']}")

    # Tab 3: Hotels with static images
    with tab3:
        st.subheader("🏨 Hotel Options")
        hotels = memory.get("HotelAgent", {}).get("hotels", [])
        hotel_images = {
            "Hilton Makkah": "https://images.unsplash.com/photo-1558959357-685f9c7ace7b",
            "Swissotel Makkah": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb",
            "Al Safwah Hotel": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b"
        }
        for h in hotels:
            img = hotel_images.get(h["name"], hotel_images["Hilton Makkah"])
            maps_link = f"https://www.google.com/maps/search/?api=1&query={h['name'].replace(' ', '+')}+Makkah"
            st.image(img, width=600, caption=h["name"])
            st.markdown(f"- **Price**: ${h['price_per_night']}")
            st.markdown(f"- **Distance to Kaaba**: {h['distance_to_kaaba']}")
            st.markdown(f"- **Rating**: {h['rating']} ⭐️")
            st.markdown(f"[🗺 View on Google Maps]({maps_link})")
            st.markdown("---")

    # Tab 4: Restaurants with reliable images
    with tab4:
        st.subheader("🍽️ Restaurant Options")
        restaurants = memory.get("FoodAgent", {}).get("restaurants", [])
        restaurant_images = {
            "Al Baik": "https://cdn.pixabay.com/photo/2017/05/07/08/56/chicken-2290747_1280.jpg",
            "The Oasis Restaurant": "https://cdn.pixabay.com/photo/2015/04/08/13/13/food-712665_1280.jpg",
            "Al Tazaj": "https://cdn.pixabay.com/photo/2017/12/09/08/18/roasted-chicken-3005985_1280.jpg"
        }
        for r in restaurants:
            img = restaurant_images.get(
                r["name"],
                "https://cdn.pixabay.com/photo/2016/03/05/19/02/hamburger-1238246_1280.jpg"
            )
            maps_link = f"https://www.google.com/maps/search/?api=1&query={r['name'].replace(' ', '+')}+Makkah"
            st.image(img, width=600, caption=r["name"])
            st.markdown(f"- **Type**: {r['type']}")
            st.markdown(f"- **Distance**: {r['distance']}")
            st.markdown(f"- **Rating**: {r['rating']} ⭐️")
            st.markdown(f"[🗺 View on Google Maps]({maps_link})")
            st.markdown("---")

    # Tab 5: Itinerary
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
