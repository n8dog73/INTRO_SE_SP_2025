from django.urls import path
from . import views

urlpatterns = [
    path ('', views.home, name='home'),
    path ('products', views.home),
    path ('home', views.home),
    path ('sign-up', views.sign_up, name='sign_up'),
   
]