from django.db import models
from django.conf import settings

class Workshop(models.Model):
    CATEGORY_CHOICES = [
        ('Technology', 'Technology'),
        ('Business', 'Business'),
        ('Soft Skills', 'Soft Skills'),
        ('AI / ML', 'AI / ML'),
        ('Cloud', 'Cloud'),
        ('Programming', 'Programming'),
        ('Design', 'Design'),
        ('Other', 'Other')
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Technology')
    seat_limit = models.PositiveIntegerField()
    speaker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='assigned_workshops')
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='workshop_images/', blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_workshops')
    # ... fields ...
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['start_date']),
            models.Index(fields=['category']),
            models.Index(fields=['speaker']),
        ]

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Session(models.Model):
    MODE_CHOICES = (
        ('online', 'Online'),
        ('offline', 'Offline'),
    )
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='sessions')
    session_title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    day_of_week = models.CharField(max_length=20) # e.g., "Monday" or date? Prompt says "day_of_week"
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='offline')

    def __str__(self):
        return f"{self.session_title} ({self.workshop.title})"

from django.core.validators import MinValueValidator, MaxValueValidator

class WorkshopRating(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('workshop', 'user')
        indexes = [
            models.Index(fields=['rating']),
        ]

    def __str__(self):
        return f"{self.rating} - {self.workshop.title}"
