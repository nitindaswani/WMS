from django.db import models
from attendance.models import Registration
import uuid

class Certificate(models.Model):
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE, related_name='certificate')
    certificate_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    issue_date = models.DateField(auto_now_add=True)
    template_path = models.CharField(max_length=255, default='certificates/templates/default.png')
    file = models.FileField(upload_to='certificates/generated/', blank=True, null=True)

    def __str__(self):
        return f"Certificate for {self.registration.user.full_name}"
