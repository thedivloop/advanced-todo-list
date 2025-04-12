from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Todo(models.Model):

  PRIORITY_CHOICES = (
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
  ) 
  STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('In Progress', 'In Progress'),
    ('Completed', 'Completed'),
  )

  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos', default=None)

  title = models.CharField(max_length=255)
  description = models.TextField(blank=True, null=True)
  due_date = models.DateField(null=True, blank=True)
  priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
  duration = models.IntegerField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  time_completion = models.IntegerField(null=True, blank=True)
  time_spent = models.IntegerField(null=True, blank=True)
  time_remaining = models.IntegerField(null=True, blank=True)

  def __str__(self):
    return self.title