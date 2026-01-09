from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class FertilizerPrediction(models.Model):
    """
    Model to store fertilizer prediction history based on sensor readings.
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='fertilizer_predictions',
        null=True, 
        blank=True
    )
    
    # Sensor readings at the time of prediction
    temperature = models.FloatField(help_text="Temperature in Celsius")
    humidity = models.FloatField(help_text="Humidity percentage", null=True, blank=True)
    moisture = models.FloatField(help_text="Soil moisture percentage")
    soil_ph = models.FloatField(help_text="Soil pH value", null=True, blank=True)
    ec = models.FloatField(help_text="Electrical Conductivity", null=True, blank=True)
    nitrogen = models.FloatField(help_text="Nitrogen level")
    phosphorous = models.FloatField(help_text="Phosphorus level")
    potassium = models.FloatField(help_text="Potassium level")
    soil_type = models.CharField(max_length=50, help_text="Soil type", null=True, blank=True)
    crop_type = models.CharField(max_length=50, help_text="Crop type", null=True, blank=True)

    # Prediction results
    recommended_fertilizer = models.CharField(
        max_length=255, 
        help_text="Recommended fertilizer name/type"
    )
    fertilizer_amount = models.FloatField(
        help_text="Recommended amount in kg/hectare",
        null=True,
        blank=True
    )
    confidence_score = models.FloatField(
        help_text="Prediction confidence score (0-1)",
        null=True,
        blank=True
    )
    recommendation_details = models.TextField(
        help_text="Detailed recommendation explanation",
        null=True,
        blank=True
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Fertilizer Prediction"
        verbose_name_plural = "Fertilizer Predictions"
    
    def __str__(self):
        return f"Prediction: {self.recommended_fertilizer} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
