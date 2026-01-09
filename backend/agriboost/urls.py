# agriboost/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # All API routes under /api/
    path("api/users/", include("users.urls")),      # register/login
    path("api/disease/", include("disease.urls")),    # your disease app
    path("api/sensors/", include("sensors.urls")),    # your sensors app
]
