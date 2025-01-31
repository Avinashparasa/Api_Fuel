from django.urls import path
from .views import RouteAPI

urlpatterns = [
    path('route/', RouteAPI.as_view(), name='route-api'),  # Ensure this is correctly written
]
