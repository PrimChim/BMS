from .views import create_bill
from django.urls import path

app_name = 'billing'
urlpatterns = [
    path('create-bill/', create_bill, name='create-bill'),
]