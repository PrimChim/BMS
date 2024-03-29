# urls.py for users app
from django.urls import path
from .views import register_api, login_api, general_view, get_customers, add_customer, all_users, logout_api

app_name = 'users'
urlpatterns = [
    path('register-api', register_api, name='register_api'),
    path('api/login', login_api, name='login_api'),
    path('api/logout', logout_api, name='logout_api'),
    path('', general_view, {'slug': 'index'},name='index'),
    path('<slug:slug>', general_view , name='general'),
    path('customers', get_customers, name='customers-api'),
    path('add-customer', add_customer, name='add-customer'),
    path('api/users', all_users, name='users-api'),
]