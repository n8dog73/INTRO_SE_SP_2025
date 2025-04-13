from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.views.cart_summary, name="cart_summary"),
    path('cart_summary/', views.cart_summary, name="cart_summary"),
    #path('add/', views.views.add_to_cart, name="add_to_cart"),
    #path('delete/', views.views.remove_from_cart, name="delete_from_cart"),
    path('update/', views.update_cart, name="update_cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('checkout-success/', views.checkout_success, name="checkout_success"),
    path('add/<int:product_id>/', views.add_to_cart, name="add_to_cart"),
    #path('remove/<int:item_id>/', views.remove_from_cart, name="remove_from_cart"),  
    path('cart/clear/', views.clear_cart, name='clear_cart'),
]