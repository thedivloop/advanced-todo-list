from django.urls import path
from . import views

app_name = 'todos'

urlpatterns = [
  path('', views.index, name='index'),
  path('new/', views.new, name='new'),
  path('<int:pk>/', views.detail, name='detail'),
  path('<int:pk>/update/', views.update, name='update'),
  path('<int:pk>/delete/', views.delete, name='delete'),

  # Timer endpoints
  path('<int:pk>/timer/start/', views.start_timer, name='start_timer'),
  path('<int:pk>/timer/stop/', views.stop_timer, name='stop_timer'),
  path('<int:pk>/timer/status/', views.get_timer_status, name='timer_status'),
  path('timer/check-active/', views.check_active_timer, name='check_active_timer'),
]