from django.contrib import admin
from .models import Product, Seller

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacture', 'model_number', 'price', 'quantity', 'category', 'created_at')
    search_fields = ('name', 'manufacture', 'model_number', 'category')
    list_filter = ('category',)
    ordering = ('-created_at',)
    list_per_page = 10
    list_editable = ('price', 'quantity')
