from django.db import models
from django.contrib.auth.models import User


class MedicineData(models.Model):
    """Model to store medicine data for recommendations"""
    medicine_name = models.CharField(max_length=200)
    description = models.TextField()
    usage = models.TextField()
    side_effects = models.TextField()
    precautions = models.TextField()
    category = models.CharField(max_length=100)
    
    def __str__(self):
        return self.medicine_name


class PatientQuery(models.Model):
    """Model to store patient queries and recommendations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    symptoms = models.TextField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    medical_history = models.TextField(blank=True)
    recommended_medicines = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Query {self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['-created_at']
