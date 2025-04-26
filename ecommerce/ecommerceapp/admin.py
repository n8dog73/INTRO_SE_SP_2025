from django.contrib import admin
from .models import Seller, UserProfile, Product, Category, PurchaseOrder
from django.contrib.auth.models import User

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacture', 'model_number', 'price', 'quantity', 'category', 'created_at')
    search_fields = ('name', 'manufacture', 'model_number', 'category')
    list_filter = ('category',)
    ordering = ('-created_at',)
    list_per_page = 10
    list_editable = ('price', 'quantity')

admin.site.register(Seller)
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(PurchaseOrder)


class UserProflieAttributes(admin.StackedInline):
    model = UserProfile
    
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ['username', 'email', 'first_name', 'last_name']
    inlines = [UserProflieAttributes]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)