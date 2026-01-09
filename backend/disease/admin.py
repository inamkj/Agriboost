from django.contrib import admin
from .models import DiseaseHistory

@admin.register(DiseaseHistory)
class DiseaseHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "label", "confidence", "created_at")
    list_filter = ("label", "created_at")
    search_fields = ("user__email", "label")
    readonly_fields = ("created_at",)
