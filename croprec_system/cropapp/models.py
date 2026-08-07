from django.db import models
from django.contrib.auth.models import User

# Stores user role (Farmer / Researcher)
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('Farmer', 'Farmer'),
        ('Researcher', 'Researcher'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class CropRecord(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)
    N = models.FloatField()
    P = models.FloatField()
    K = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    ph = models.FloatField()
    rainfall = models.FloatField()
    predicted_crop = models.CharField(max_length=100)
    recommended_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.predicted_crop} - {self.farmer.username}"
    
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    rating = models.IntegerField(choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')])
    blank=False
    null=False
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.subject
