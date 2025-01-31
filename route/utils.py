import requests
import pandas as pd
import os

def load_fuel_data():
    """Load fuel prices from the CSV file."""
    file_path = os.path.join(os.path.dirname(__file__), "fuel_prices.csv")
    
    try:
        fuel_data = pd.read_csv(file_path)
        return fuel_data
    except FileNotFoundError:
        print("Error: Fuel price file not found.")
        return None


# def get_route(start, finish):
#     """Mock route data for testing."""
#     return {
#         "routes": [
#             {
#                 "summary": {
#                     "distance": 4480500,  # Distance in meters (4480.5 km)
#                     "duration": 144000  # Duration in seconds (40 hours)
#                 }
#             }
#         ]
#     }
import requests
import logging

logger = logging.getLogger(__name__)

def get_route(start, finish, api_key):
    """Fetch route from Google Maps Directions API."""
    url = "https://maps.gomaps.pro/maps/api/directions/json"
    params = {
        "origin": start,  # Start coordinates (e.g., "-74.006,40.7128")
        "destination": finish,  # End coordinates (e.g., "-118.2437,34.0522")
        "key": api_key,  # Your Google Maps API key
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
        data = response.json()

        # Check if the API returned a valid response
        if data["status"] == "OK":
            return data
        else:
            logger.error(f"Google Maps API Error: {data['status']}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request Exception: {e}")
        return None
def optimize_fuel_stops(route_distance, fuel_data, mpg=10, tank_range=500):
    
    if fuel_data is None or fuel_data.empty:
        return [], 0

    fuel_stops = []
    total_cost = 0
    remaining_distance = route_distance / 1609.34  # Convert meters to miles

    while remaining_distance > 0:
        
        best_station = fuel_data.loc[fuel_data["Retail Price"].idxmin()]
        fuel_stops.append({
            "location": f"{best_station['City']}, {best_station['State']}",
            "price": best_station["Retail Price"],
            "station": best_station["Truckstop Name"],
        })

        # Deduct distance covered in this leg
        remaining_distance -= tank_range
        total_cost += (tank_range / mpg) * best_station["Retail Price"]

    return fuel_stops, total_cost
