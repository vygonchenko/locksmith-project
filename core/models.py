from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class CallbackRequest(models.Model):
    name = models.CharField(max_length=100)
    phone = PhoneNumberField()
    preferred_time = models.CharField(max_length=50)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Callback from {self.name} at {self.created_at}"