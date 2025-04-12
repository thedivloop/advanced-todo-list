from django import forms
from .models import Todo

class NewTodoForm(forms.ModelForm):
  class Meta:
    model = Todo
    # exclude = ['user']
    fields = ('title', 'description', 'priority', 'status', 'due_date', 'duration', 'time_completion', 'time_spent', 'time_remaining')
    widgets = {
      'due_date': forms.DateInput(attrs={'type': 'date'}),
    }
    labels = {
      'title': 'Title',
      'description': 'Description',
      'priority': 'Priority',
      'status': 'Status',
      'due_date': 'Due Date',
      'duration': 'Duration',
      'time_completion': 'Completion rate',
      'time_spent': 'Time Spent',
      'time_remaining': 'Time Remaining',
    }
    help_texts = {
      'title': 'Enter the title of the todo item.',
      'description': 'Enter a brief description of the todo item.',
      'priority': 'Select the priority level.',
      'status': 'Select the current status of the todo item.',
      'due_date': 'Select the due date for this todo item.',
      'duration': 'Enter the estimated duration in minutes for this todo item.',
      'time_completion': 'Enter the completion rate in %.',
      'time_spent': 'Enter the time spent on this todo item.',
    }
    error_messages = {
      'title': {
        'max_length': "This title is too long.",
        'required': "This field is required.",
      },
      'description': {
        'max_length': "This description is too long.",
      },
      'due_date': {
        'invalid': "Enter a valid date.",
      },
      'duration': {
        'invalid': "Enter a valid duration.",
      },
      'time_completion': {
        'invalid': "Enter a valid time completion.",
      },
      'time_spent': {
        'invalid': "Enter a valid time spent.",
      },
      'time_remaining': {
        'invalid': "Enter a valid time remaining.",
      },
    }

class UpdateTodoForm(forms.ModelForm):
  class Meta:
    model = Todo
    fields = ('title', 'description', 'priority', 'status', 'due_date', 'duration', 'time_completion', 'time_spent', 'time_remaining')
    widgets = {
      'due_date': forms.DateInput(attrs={'type': 'date'}),
    }
    labels = {
      'title': 'Title',
      'description': 'Description',
      'priority': 'Priority',
      'status': 'Status',
      'due_date': 'Due Date',
      'duration': 'Duration',
      'time_completion': 'Completion rate',
      'time_spent': 'Time Spent',
      'time_remaining': 'Time Remaining',
    }
    help_texts = {
      'title': 'Enter the title of the todo item.',
      'description': 'Enter a brief description of the todo item.',
      'priority': 'Select the priority level.',
      'status': 'Select the current status of the todo item.',
      'due_date': 'Select the due date for this todo item.',
      'duration': 'Enter the estimated duration in minutes for this todo item.',
      'time_completion': 'Enter the completion rate in %.',
      'time_spent': 'Enter the time spent on this todo item.',
      'time_remaining': 'Enter the time remaining for this todo item.',
    }
    error_messages = {
      'title': {
        'max_length': "This title is too long.",
        'required': "This field is required.",
      },
      'description': {
        'max_length': "This description is too long.",
      },
      'due_date': {
        'invalid': "Enter a valid date.",
      },
      'duration': {
        'invalid': "Enter a valid duration.",
      },
      'time_completion': {
        'invalid': "Enter a valid time completion.",
      },
      'time_spent': {
        'invalid': "Enter a valid time spent.",
      },
      'time_remaining': {
        'invalid': "Enter a valid time remaining.",
      },
    }
