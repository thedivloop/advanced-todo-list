from django import forms
from .models import Todo, TaskGroup

class NewTodoForm(forms.ModelForm):
  class Meta:
    model = Todo
    # exclude = ['user']
    fields = ('title', 'description', 'priority', 'status', 'due_date', 'duration', 'group', 'time_completion', 'time_spent', 'time_remaining')
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
  def __init__(self, *args, **kwargs):
    user = kwargs.pop('user', None)
    super().__init__(*args, **kwargs)
    if user:
      self.fields['group'].queryset = TaskGroup.objects.filter(user=user)
      self.fields['group'].required = False

class UpdateTodoForm(forms.ModelForm):
  class Meta:
    model = Todo
    fields = ('title', 'description', 'priority', 'status', 'due_date', 'duration', 'group', 'time_completion', 'time_spent', 'time_remaining')
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
  def __init__(self, *args, **kwargs):
    user = kwargs.pop('user', None)
    super().__init__(*args, **kwargs)
    if user:
      self.fields['group'].queryset = TaskGroup.objects.filter(user=user)
      self.fields['group'].required = False

class TaskGroupForm(forms.ModelForm):
  class Meta:
    model = TaskGroup
    fields = ('name', 'description', 'color')
    widgets = {
        'color': forms.TextInput(attrs={'type': 'color'}),
        'description': forms.Textarea(attrs={'rows': 3}),
    }
    labels = {
        'name': 'Group Name',
        'description': 'Description (Optional)',
        'color': 'Color',
    }
    help_texts = {
        'name': 'Enter a unique name for this group.',
        'color': 'Choose a color to identify this group.',
    }
  
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user', None)
    super().__init__(*args, **kwargs)
  
  def clean_name(self):
    name = self.cleaned_data.get('name')
    if self.user:
      # Check for duplicate group name for this user
      existing = TaskGroup.objects.filter(user=self.user, name=name)
      if self.instance.pk:
        existing = existing.exclude(pk=self.instance.pk)
      if existing.exists():
        raise forms.ValidationError(f'You already have a group named "{name}".')
    return name