from django.urls import reverse_lazy

LOGIN_URL = reverse_lazy('users:login')
REGISTER_URL = reverse_lazy('users:register')
DASHBOARD_URL = reverse_lazy('users:dashboard')
TODOS_URL = reverse_lazy('todos:index')
LOGOUT_URL = reverse_lazy('users:logout')

DASHBOARD_TEMPLATE = 'users/dashboard.html'
LOGIN_TEMPLATE = 'users/login.html'
REGISTER_TEMPLATE = 'users/register.html'

MENU_LIST = [{'name': 'Home','uri': '/'}, 
             {'name': 'Features','uri': '/features/'}, 
             {'name': 'About','uri': '/about/'}, 
             {'name': 'Login','uri': LOGIN_URL}, 
             {'name': 'Register','uri': REGISTER_URL}]