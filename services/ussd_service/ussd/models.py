from django.db import models
from django.utils import timezone


class USSDUser(models.Model):
    '''
    Stores basic user details who access the platform via USSD.
    '''
    phone_number = models.CharField(max_length=15, unique=True)
    language = models.CharField(max_length=5, default='en')
    location = models.CharField(max_length=100, blank=True, null=True)
    registered_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.phone_number} ({self.language})"


class USSDSession(models.Model):
    '''
    Keeps track of an active USSD session for a user.
    '''
    user = models.ForeignKey(USSDUser, on_delete=models.CASCADE, related_name='sessions')
    session_id = models.CharField(max_length=100, unique=True)
    last_input = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Session {self.session_id} for {self.user.phone_number}"
