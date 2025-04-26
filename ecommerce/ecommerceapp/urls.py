from django.urls import path, include
from . import views

urlpatterns = [
    path ('', views.home, name='home'),
    path ('products', views.home),
    path ('home', views.home),
    path ('sign-up', views.sign_up, name='sign_up'),
    path('logout/', views.logout_user, name='logout'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('add_seller/', views.add_seller, name='add_seller'),
    path('cart/', include('cart.urls')),
    path('delete_account/', views.delete_account, name='delete_account'),
    #path('checkout/', views.checkout, name='checkout'),
    path('order-tracking/', views.order_tracking, name='order_tracking'),
    #path('', views.cart_summary, name='cart_summary'),
   
]