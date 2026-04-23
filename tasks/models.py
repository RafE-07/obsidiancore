from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Task(models.Model):
    IMPORTANCE_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    IMPORTANCE_COLORS = {
        'low': '#00ff00',        
        'medium': '#ffff00',   
        'high': '#ff8800',     
        'critical': '#ff0000',   
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    due_datetime = models.DateTimeField()
    importance = models.CharField(max_length=10, choices=IMPORTANCE_CHOICES, default='medium')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']   
    def __str__(self):
        return self.title

    def is_expired(self):
        """Return True if not completed and due date is in the past."""
        return not self.completed and self.due_datetime < timezone.now()

    def remaining_time(self):
        """Return a human-readable string of time left (or 'Expired')."""
        if self.completed:
            return "Completed"
        now = timezone.now()
        if self.due_datetime < now:
            return "Expired"
        delta = self.due_datetime - now
        total_seconds = int(delta.total_seconds())
        days, remainder = divmod(total_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, _ = divmod(remainder, 60)
        if days:
            return f"{days}d {hours}h"
        if hours:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"