from django.db import models
from django.conf import settings

class DiseaseHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   
    label = models.CharField(max_length=100)
    confidence = models.FloatField()
    recommendation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.label} ({self.confidence:.2f})"
