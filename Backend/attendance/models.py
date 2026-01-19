from django.db import models
from django.conf import settings
from workshops.models import Workshop, Session
import uuid

class Registration(models.Model):
    TYPE_CHOICES = (
        ('student', 'Student'),
        ('speaker', 'Speaker'),
    )
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='registrations')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='student')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('workshop', 'user')

    def __str__(self):
        return f"{self.user.full_name} - {self.workshop.title}"

class Attendance(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='attendance_records')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True, related_name='attendance_records')
    timestamp = models.DateTimeField(auto_now_add=True)
    qr_secret = models.CharField(max_length=255, blank=True, null=True)
    is_present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('registration', 'session')
        indexes = [
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"Attendance {self.registration.user.full_name} at {self.timestamp}"
