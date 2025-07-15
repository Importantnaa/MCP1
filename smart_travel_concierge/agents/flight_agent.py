# flight_agent.py

def get_mock_flights(origin, destination, depart_date, return_date):
    flights = [
        {
            "airline": "Saudia",
            "price": 420,
            "depart": depart_date,
            "return": return_date,
            "duration": "12h 30m"
        },
        {
            "airline": "Emirates",
            "price": 450,
            "depart": depart_date,
            "return": return_date,
            "duration": "13h"
        },
        {
            "airline": "Qatar Airways",
            "price": 480,
            "depart": depart_date,
            "return": return_date,
            "duration": "11h 50m"
        }
    ]

    return {"flights": sorted(flights, key=lambda x: x["price"])}


# Run directly to test
if __name__ == "__main__":
    mock_data = get_mock_flights("JFK", "JED", "2025-12-10", "2025-12-15")
    import json
    print(json.dumps(mock_data, indent=2))
