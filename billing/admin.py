from django.contrib import admin
from .models import Items, Bills, BillItems, Business

# Register your models here.

class ItemsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    search_fields = ('name',)
    list_filter = ('name', 'price', 'description')

class BillsAdmin(admin.ModelAdmin):
    list_display = ('id','bill_no', 'customer_id', 'total_price', 'invoice_date')
    search_fields = ('id', 'bill_no', 'customer_id',)
    list_filter = ('id','bill_no', 'customer_id', 'total_price', 'invoice_date')

class BillItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'quantity')
    search_fields = ('id',)
    list_filter = ('id', 'quantity')

class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'email', 'website')
    search_fields = ('name', 'address', 'phone', 'email', 'website')
    list_filter = ('name', 'address', 'phone', 'email', 'website')

admin.site.register(Items, ItemsAdmin)
admin.site.register(Bills, BillsAdmin)
admin.site.register(BillItems, BillItemsAdmin)
admin.site.register(Business, BusinessAdmin)