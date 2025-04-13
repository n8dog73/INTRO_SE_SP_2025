from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate

def home(request):
    products = Product.objects.all()
    return render(request, 'main/home.html', {'products': products})

def sign_up(request):
    if request.method == 'POST':
        # Handle the sign-up logic here
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {'form': form})