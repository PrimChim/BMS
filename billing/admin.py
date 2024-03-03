from django.contrib import admin
from .models import Items, Bills, BillItems

# Register your models here.

class ItemsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    search_fields = ('name',)
    list_filter = ('name', 'price', 'description')

class BillsAdmin(admin.ModelAdmin):
    list_display = ('id','customer_id', 'total_price', 'invoice_date')
    search_fields = ('id', 'customer_id',)
    list_filter = ('id','customer_id', 'total_price', 'invoice_date')

class BillItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'quantity')
    search_fields = ('id',)
    list_filter = ('id', 'quantity')

admin.site.register(Items, ItemsAdmin)
admin.site.register(Bills, BillsAdmin)
admin.site.register(BillItems, BillItemsAdmin)