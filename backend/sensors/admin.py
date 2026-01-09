from django.contrib import admin
from .models import FertilizerPrediction


@admin.register(FertilizerPrediction)
class FertilizerPredictionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'recommended_fertilizer', 'fertilizer_amount', 'confidence_score', 'created_at']
    list_filter = ['created_at', 'recommended_fertilizer']
    search_fields = ['user__email', 'recommended_fertilizer', 'recommendation_details']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Sensor Readings', {
            'fields': ('temperature', 'humidity', 'soil_moisture', 'soil_ph', 'ec', 'nitrogen', 'phosphorus', 'potassium')
        }),
        ('Prediction Results', {
            'fields': ('recommended_fertilizer', 'fertilizer_amount', 'confidence_score', 'recommendation_details')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
