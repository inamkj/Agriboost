from rest_framework import serializers
from .models import FertilizerPrediction


class FertilizerPredictionSerializer(serializers.ModelSerializer):
    """Serializer for fertilizer prediction history."""
    
    user_email = serializers.EmailField(source='user.email', read_only=True, required=False)
    
    class Meta:
        model = FertilizerPrediction
        fields = [
            'id',
            'user',
            'user_email',
            'temperature',
            'humidity',
            'moisture',
            'soil_ph',
            'ec',
            'nitrogen',
            'phosphorous',
            'potassium',
            'recommended_fertilizer',
            'fertilizer_amount',
            'confidence_score',
            'recommendation_details',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class FertilizerPredictionCreateSerializer(serializers.Serializer):
    """Serializer for creating fertilizer predictions from sensor data."""
    
    temperature = serializers.FloatField()
    humidity = serializers.FloatField(required=False, allow_null=True)
    moisture = serializers.FloatField()
    crop_type = serializers.CharField(default="Sugarcane")
    soil_type = serializers.ChoiceField(choices=[
        ('Loamy', 'Loamy'),
        ('Clayey', 'Clayey'),
        ('Sandy', 'Sandy'),
        ('Black', 'Black'),
        ('Red', 'Red')
        
    ])
    nitrogen = serializers.FloatField()
    potassium = serializers.FloatField()
    phosphorous = serializers.FloatField()
    
    


