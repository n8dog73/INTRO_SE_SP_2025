from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.views.cart_summary, name="cart_summary"),
    path('add/', views.views.add_to_cart, name="add_to_cart"),
    path('delete/', views.views.remove_from_cart, name="delete_from_cart"),
    path('update/', views.views.update_cart, name="update_cart"),
    path('checkout/', views.views.checkout, name="checkout"),
    path('checkout/success/', views.views.checkout_success, name="checkout_success"),  
    
]