import streamlit as st
import json
from pathlib import Path

RESULT_PATH = Path("mcp_result.json")
MEMORY_PATH = Path("smart_travel_concierge/memory_store.json")

def load_json(file_path):
    if file_path.exists():
        with open(file_path) as f:
            return json.load(f)
    return {}

# --- Streamlit UI setup ---
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
    .stTextInput input, .stSelectbox div div input, .stMultiSelect div div div {
        background-color: #252633; color: white; border-radius: 5px;
    }
    button[kind="primary"] {
        background-color: #ffd700; color: #000; border-radius: 25px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌍 Smart Travel Concierge — Premium Edition")
st.markdown("Plan your luxury journey with tailored recommendations and visual previews.")

# --- Sidebar: User Preferences ---
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

# --- Load orchestrator output ---
result = load_json(RESULT_PATH)

if result:
    memory = result.get("memory", {})

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Overview", "🛫 Flights", "🏨 Hotels", "🍽️ Food", "📅 Itinerary"])

    with tab1:
        st.subheader("📋 Trip Summary")
        st.json(memory.get("PlannerAgent", {}))

    with tab2:
        st.subheader("🛫 Flights")
        flights = memory.get("FlightAgent", {}).get("flights", [])
        for f in flights:
            st.markdown(f"**{f['airline']}** — ${f['price']} — Depart: {f['depart']} — Return: {f['return']}")

    with tab3:
        st.subheader("🏨 Hotel Options")
        hotels = memory.get("HotelAgent", {}).get("hotels", [])
        for h in hotels:
            st.image("https://source.unsplash.com/featured/?luxuryhotel", width=600, caption=h["name"])
            st.markdown(f"- **Price**: ${h['price_per_night']}")
            st.markdown(f"- **Distance to Kaaba**: {h['distance_to_kaaba']}")
            st.markdown(f"- **Rating**: {h['rating']} ⭐️")
            st.markdown("---")

    with tab4:
        st.subheader("🍽️ Restaurant Options")
        restaurants = memory.get("FoodAgent", {}).get("restaurants", [])
        for r in restaurants:
            st.image("https://source.unsplash.com/featured/?halalfood", width=600, caption=r["name"])
            st.markdown(f"- **Type**: {r['type']}")
            st.markdown(f"- **Distance**: {r['distance']}")
            st.markdown(f"- **Rating**: {r['rating']} ⭐️")
            st.markdown("---")

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
