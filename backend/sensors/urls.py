"""
URL patterns for the sensors app API endpoints.
"""

from django.urls import path
from .views import SensorFeedView, FertilizerPredictView, FertilizerHistoryView

urlpatterns = [
    path("feed/", SensorFeedView.as_view(), name="sensor-feed"),
    path("predict/", FertilizerPredictView.as_view(), name="fertilizer-predict"),
    path("predictions/", FertilizerHistoryView.as_view(), name="fertilizer-history"),
]
