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
    created_at = models.DateTimeField(auto_now_add=True)

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

class WorkshopRating(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField() # 1-5 validation can be in serializer
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} - {self.workshop.title}"
