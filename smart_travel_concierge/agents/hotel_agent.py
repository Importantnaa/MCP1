# hotel_agent.py

def get_mock_hotels(location, checkin, checkout, budget_level):
    # Mock hotel dataset (can be dynamically generated later)
    hotels = [
        {
            "name": "Hilton Makkah",
            "price_per_night": 120,
            "distance_to_kaaba": "200m",
            "rating": 4.6
        },
        {
            "name": "Swissotel Makkah",
            "price_per_night": 100,
            "distance_to_kaaba": "250m",
            "rating": 4.5
        },
        {
            "name": "Al Safwah Hotel",
            "price_per_night": 90,
            "distance_to_kaaba": "180m",
            "rating": 4.4
        }
    ]

    # Filter and return cheapest 3 sorted by price
    return {
        "hotels": sorted(hotels, key=lambda h: h["price_per_night"])[:3]
    }


# ✅ Test this file directly
if __name__ == "__main__":
    hotels = get_mock_hotels("Makkah", "2025-12-10", "2025-12-15", "low")
    import json
    print(json.dumps(hotels, indent=2))
