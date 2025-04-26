from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserProfile, Product, Seller, PurchaseOrder, OrderItem
from .forms import RegisterForm, UserProfileForm, SellerForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
            return redirect('/update_profile')  # Redirect to the update profile page
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {'form': form})

def update_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)  # Get the current user's UserProfile
    #user_profile = request.user.userprofile  # Get the current user's UserProfile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the home page or another page
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'registration/update_profile.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('/home')

def add_seller(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = SellerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Seller added successfully.")
            return redirect('home')  # Or any success page
    else:
        form = SellerForm()

    return render(request, 'main/add_seller.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  # Log out the user before deleting
        user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home')  # or wherever you want to send them after deletion

    return render(request, 'registration/delete_account.html')

def order_tracking(request):
    orders = PurchaseOrder.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_tracking.html', {'orders': orders})