from django.contrib import admin

# Register your models here.
from todos.models import Todo
from todos.models import TaskGroup

admin.site.register(Todo)
admin.site.register(TaskGroup)