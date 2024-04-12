from .views import create_bill, add_items, get_items, view_bills, create_bill_api, view_bills_frontend, dashboard
from django.urls import path

app_name = 'billing'
urlpatterns = [
    # billing frontend views urls
    path('create-bill/', create_bill, name='create-bill'),
    path('bills/', view_bills_frontend, name='view-bills-frontend'),
    path('dashboard/', dashboard, name='dashboard'),

    # billing API urls
    path('api/add-items/', add_items, name='add-items'),
    path('api/get-items/', get_items, name='get-items'),
    path('api/view-bills/', view_bills, name='view-bills'),
    path('api/view-bills/<int:id>', view_bills, name='view-bills'),
    path('api/create-bill-api/',create_bill_api,name='create-bill-api')
]