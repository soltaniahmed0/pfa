from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class AnalysisHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classifier_analysis_history')
    image = models.ImageField(upload_to='analysis_images/')
    disease_name = models.CharField(max_length=100)
    confidence = models.FloatField()
    is_healthy = models.BooleanField()
    treatment_recommendation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}'s analysis on {self.created_at}"
