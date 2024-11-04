# activity_logs/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone

class UserActivityLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='activity_logs'
    )
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    extra_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp}"
    
    def formatted_extra_data(self):
        if isinstance(self.extra_data, dict):
            return ", ".join([f"{key}: {value}" for key, value in self.extra_data.items()])
        return self.extra_data
