from django.urls import reverse

LOGIN_URL = reverse('users:login')
REGISTER_URL = reverse('users:register')
DASHBOARD_URL = reverse('users:dashboard')
LOGOUT_URL = reverse('users:logout')

LOGIN_TEMPLATE = 'users/login.html'
REGISTER_TEMPLATE = 'users/register.html'

MENU_LIST = [{'name': 'Home','uri': '/'}, 
             {'name': 'Features','uri': '/features/'}, 
             {'name': 'About','uri': '/about/'}, 
             {'name': 'Login','uri': LOGIN_URL}, 
             {'name': 'Register','uri': REGISTER_URL}]