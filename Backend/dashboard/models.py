from django.db import models

class DashboardMetrics(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    total_workshops = models.PositiveIntegerField(default=0)
    total_students = models.PositiveIntegerField(default=0)
    total_speakers = models.PositiveIntegerField(default=0)
    total_budget = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_attendees = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = "Dashboard Metrics"

    def __str__(self):
        return f"Metrics at {self.timestamp}"
