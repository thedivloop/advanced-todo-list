from django import forms
from .models import Todo

class NewTodoForm(forms.ModelForm):
  class Meta:
    model = Todo
    fields = ('title', 'description')

class UpdateTodoForm(forms.ModelForm):
  class Meta:
    model = Todo
    fields = ('title', 'description')
