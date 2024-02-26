# urls.py for users app
from django.urls import path
from .views import register, register_api, login_api, login_view, CustomerViewSet, add_customer

app_name = 'users'
urlpatterns = [
    path('register_api', register_api, name='register_api'),
    path('register', register, name='register'),
    path('login_api', login_api, name='login_api'),
    path('login', login_view, name='login'),
    path('customers', CustomerViewSet.as_view({'get': 'list'}), name='customers'),
    path('add-customer', add_customer, name='add-customer'),
]