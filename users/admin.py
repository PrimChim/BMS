from django.contrib import admin
from .models import Customer

# Register your models here.

admin.site.site_header = "Khata Admin"
admin.site.site_title = "Khata Admin Portal"
admin.site.index_title = "Welcome to Khata"

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'pan', 'email', 'address')
    search_fields = ('name', 'pan', 'email')
    list_filter = ('name', 'pan', 'email', 'address')

admin.site.register(Customer, CustomerAdmin)