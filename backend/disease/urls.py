from django.urls import path
from .views import PredictDiseaseView, UserDiseaseHistoryView

urlpatterns = [
     path("predict/", PredictDiseaseView.as_view(), name="disease-predict"),
      path("crop-history/", UserDiseaseHistoryView.as_view(), name="user-disease-history"),
]
