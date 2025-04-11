from django.urls import reverse

LOGIN_URL = reverse('users:login')
REGISTER_URL = reverse('users:register')
DASHBOARD_URL = reverse('users:dashboard')
LOGOUT_URL = reverse('users:logout')

LOGIN_TEMPLATE = 'users/login.html'
REGISTER_TEMPLATE = 'users/register.html'