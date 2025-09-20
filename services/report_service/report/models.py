from django.db import models
from django.utils import timezone
from ussd.models import USSDUser


class Report(models.Model):
    '''
    Stores misinformation reports submitted by USSD users.
    '''
    user = models.ForeignKey(USSDUser, on_delete=models.CASCADE, related_name='reports')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='pening') # pending | fact_checked | dismissed

    def __str__(self):
        return f"Report {self.id} by {self.user.phone_number}"
