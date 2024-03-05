from .views import create_bill, add_items, get_items, view_bills, create_bill_api
from django.urls import path

app_name = 'billing'
urlpatterns = [
    path('create-bill/', create_bill, name='create-bill'),
    path('api/add-items/', add_items, name='add-items'),
    path('api/get-items/', get_items, name='get-items'),
    path('api/view-bills/', view_bills, name='view-bills'),
    path('api/create-bill-api/',create_bill_api,name='create-bill-api')
]