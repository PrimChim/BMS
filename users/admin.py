from django.contrib import admin
from .models import Customer, Otp

# Register your models here.

admin.site.site_header = "Khata Admin"
admin.site.site_title = "Khata Admin Portal"
admin.site.index_title = "Welcome to Khata"

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'pan', 'email', 'address')
    search_fields = ('name', 'pan', 'email')
    list_filter = ('name', 'pan', 'email', 'address')

class OtpAdmin(admin.ModelAdmin):
    list_display = ('email', 'otp', 'date')
    search_fields = ('email', 'otp')
    list_filter = ('email', 'otp', 'date')

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Otp, OtpAdmin)