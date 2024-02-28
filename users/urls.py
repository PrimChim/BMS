# urls.py for users app
from django.urls import path
from .views import register, register_api, login_api, login_view, get_customers, add_customer

app_name = 'users'
urlpatterns = [
    path('register-api', register_api, name='register_api'),
    path('register', register, name='register'),
    path('login-api', login_api, name='login_api'),
    path('login', login_view, name='login'),
    path('customers', get_customers, name='Customers API'),
    path('add-customer', add_customer, name='add-customer'),
]