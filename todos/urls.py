from django.urls import path

from . import views

app_name = 'todos'

urlpatterns = [
  path('', views.index, name='index'),
  path('new/', views.new, name='new'),
  path('<int:pk>/', views.detail, name='detail'),
  path('<int:pk>/update/', views.update, name='update'),
  path('<int:pk>/delete/', views.delete, name='delete')
]