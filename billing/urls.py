from .views import *
from django.urls import path

app_name = 'billing'
urlpatterns = [
    # billing frontend views urls
    path('create-bill/', create_bill, name='create-bill'),
    path('bills/', view_bills_frontend, name='view-bills-frontend'),
    path('dashboard/', dashboard, name='dashboard'),
    path('items/', items_frontend, name='items'),
    path('business-settings/', business_settings, name='business-settings'),

    # billing API urls
    path('api/add-items/', add_items, name='add-items'),
    path('api/get-items/', get_items, name='get-items'),
    path('api/view-bills/', view_bills, name='view-bills'),
    path('api/view-bills/<int:id>', view_bills, name='view-bills'),
    path('api/create-bill-api/',create_bill_api,name='create-bill-api'),
    path('api/cancel-bill/<int:id>', cancel_bill, name='cancel-bill'),
    path('api/update-item/<int:id>', update_item, name='update-item'),
]