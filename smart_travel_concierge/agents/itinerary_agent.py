# smart_travel_concierge/agents/itinerary_agent.py

from datetime import datetime, timedelta

def run(task_state):
    memory = task_state.get("memory", {})

    planner = memory.get("PlannerAgent", {})
    flights = memory.get("FlightAgent", {})
    hotel = memory.get("HotelAgent", {})
    food = memory.get("FoodAgent", {})

    start_date = datetime.strptime(planner["dates"]["start"], "%Y-%m-%d")
    end_date = datetime.strptime(planner["dates"]["end"], "%Y-%m-%d")
    num_days = (end_date - start_date).days + 1

    restaurant = food["restaurants"][0]["name"] if "restaurants" in food else "local halal spot"
    hotel_name = hotel.get("name", "your hotel")

    itinerary = {}

    for i in range(num_days):
        day = f"day_{i + 1}"
        date = start_date + timedelta(days=i)

        itinerary[day] = [
            f"🕌 5:30 AM: Fajr prayer at Masjid al-Haram",
            f"🍽️ 7:00 AM: Breakfast at {restaurant}",
            f"🕋 9:00 AM: Perform Umrah or visit holy sites",
            f"🛍️ 12:00 PM: Explore local markets",
            f"🛏️ 3:00 PM: Rest at {hotel_name}",
            f"🌇 6:00 PM: Maghrib prayer & dinner nearby"
        ]

    return itinerary
