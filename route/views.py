from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import get_route, load_fuel_data, optimize_fuel_stops
import logging

logger = logging.getLogger(__name__)

class RouteAPI(APIView):
    def post(self, request, *args, **kwargs):
        # Extract start and finish coordinates from the request
        start = request.data.get("start")
        finish = request.data.get("finish")

        if not start or not finish:
            return Response(
                {"error": "Both 'start' and 'finish' coordinates are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Fetch route data from Google Maps Directions API
        api_key = "AlzaSyumbNZrIEGcKN4GHgjtGeC2e8wOVk4WmWs"  # Replace with your actual API key
        route_data = get_route(start, finish, api_key)

        if not route_data:
            return Response(
                {"error": "Failed to fetch route data from Google Maps."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        # Extract route distance (in meters) from the response
        try:
            route_distance = route_data["routes"][0]["legs"][0]["distance"]["value"]
        except KeyError:
            logger.error("Invalid route data structure from Google Maps.")
            return Response(
                {"error": "Invalid route data received from Google Maps."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Load fuel data
        fuel_data = load_fuel_data()

        if fuel_data is None:
            return Response(
                {"error": "Failed to load fuel price data."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        
        fuel_stops, total_cost = optimize_fuel_stops(route_distance, fuel_data)

        
        response_data = {
            "route_distance_km": route_distance / 1000,  
            "fuel_stops": fuel_stops,
            "total_fuel_cost": total_cost,
        }

        return Response(response_data, status=status.HTTP_200_OK)