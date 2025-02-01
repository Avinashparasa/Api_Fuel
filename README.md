Fuel Route Optimization API.
This project provides an API to calculate the optimal fuel stops along a route based on fuel prices and the vehicle's fuel efficiency. It uses external routing APIs (e.g., OpenRouteService, Google Maps) to fetch route data and optimizes fuel stops to minimize costs.

Features
Route Distance Calculation: Fetches the total distance of a route between two coordinates.

Fuel Stop Optimization: Calculates the optimal fuel stops along the route based on fuel prices and vehicle efficiency.

Cost Estimation: Estimates the total fuel cost for the trip.

Integration with External APIs: Supports integration with routing APIs like OpenRouteService, Google Maps, and more.

Technologies Used
Backend: Django, Django REST Framework

Routing APIs: OpenRouteService, Google Maps (optional)

Data Handling: Pandas

Deployment: Render

Other Tools: Gunicorn, Whitenoise

Getting Started
Prerequisites
Python 3.11 or higher

Django 5.1.5 or higher

A valid API key for the routing service (e.g., OpenRouteService, Google Maps)
