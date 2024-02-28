from django.contrib import admin
from .models import Items

# Register your models here.

class ItemsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    search_fields = ('name',)
    list_filter = ('name', 'price', 'description')

admin.site.register(Items, ItemsAdmin)