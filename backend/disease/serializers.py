from rest_framework import serializers
from .models import DiseaseHistory

class DiseaseHistorySerializer(serializers.ModelSerializer):
    

    class Meta:
        model = DiseaseHistory
        fields = ['id', 'user', 'label', 'confidence', 'recommendation', 'created_at']

