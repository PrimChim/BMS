from .views import create_bill, add_items, get_items
from django.urls import path

app_name = 'billing'
urlpatterns = [
    path('create-bill/', create_bill, name='create-bill'),
    path('api/add-items/', add_items, name='add-items'),
    path('api/get-items/', get_items, name='get-items')
]