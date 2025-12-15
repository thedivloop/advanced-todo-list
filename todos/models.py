from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
  is_timer_active = models.BooleanField(default=False)
  timer_started_at = models.DateTimeField(null=True, blank=True)

  def __str__(self):
    return self.title
  
  def start_timer(self):
    """Start the timer for this task"""
    # Stop any other active timers for this user
    Todo.objects.filter(
        user=self.user, 
        is_timer_active=True
    ).exclude(pk=self.pk).update(
        is_timer_active=False,
        timer_started_at=None,
        status='Pending'
    )
    
    # Start this timer
    self.is_timer_active = True
    self.timer_started_at = timezone.now()
    self.status = 'In Progress'
    self.save()
  
  def stop_timer(self):
    """Stop the timer and update time_spent"""
    if self.is_timer_active and self.timer_started_at:
      # Calculate elapsed time in minutes
      elapsed_seconds = (timezone.now() - self.timer_started_at).total_seconds()
      elapsed_minutes = int(elapsed_seconds / 60)
      
      # Update time_spent
      self.time_spent = (self.time_spent or 0) + elapsed_minutes
      
      # Update time_remaining if duration exists
      if self.duration:
        self.time_remaining = self.duration - self.time_spent
        # Calculate completion percentage
        if self.time_spent > 0:
          self.time_completion = min(int((self.time_spent / self.duration) * 100), 100)
      
      # Reset timer fields
      self.is_timer_active = False
      self.timer_started_at = None
      self.status = 'Pending'
      self.save()
    
  def get_elapsed_time(self):
    """Get current elapsed time in seconds if timer is active"""
    if self.is_timer_active and self.timer_started_at:
      elapsed = (timezone.now() - self.timer_started_at).total_seconds()
      return int(elapsed)
    return 0
  
  @classmethod
  def get_active_timer_for_user(cls, user):
    """Get the todo with active timer for a user"""
    try:
      return cls.objects.get(user=user, is_timer_active=True)
    except cls.DoesNotExist:
      return None