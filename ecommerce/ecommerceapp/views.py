from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserProfile, Product, Seller, PurchaseOrder, OrderItem, Category
from .forms import RegisterForm, UserProfileForm, SellerForm, ProductForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q

def home(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', None)
    
    categories = Category.objects.all()

    products = Product.objects.all()
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category_id:
        products = products.filter(category_id=category_id)
    return render(request, 'main/home.html', {'products': products, 'categories': categories})

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
            seller = form.save()
            user_profile.company_name = seller
            user_profile.save()
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

@login_required
def seller_dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if not user_profile.company_name:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')
    else:
        try:
            seller = Seller.objects.get(name=user_profile.company_name)
        except Seller.DoesNotExist:
            messages.error(request, "Seller not found.")
            return redirect('home')
        products = Product.objects.filter(sellerProduct=seller)#.company_name)

        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                product.sellerProduct = seller
                product.save()
                messages.success(request, "Product added successfully.")
                return redirect('seller_dashboard')
        else:
            form = ProductForm()
            print(user_profile, products)
        return render(request, 'seller/dashboard.html', {'products': products})
    
@login_required
def add_product(request):
    user_profile = UserProfile.objects.get(user=request.user)
    print(f"User Profile: {user_profile}, Company Name: {user_profile.company_name}")

    if not user_profile.company_name:
       messages.error(request, "You do not have permission to access this page.")
       return redirect('home') 
    else:
        try:
            seller = Seller.objects.get(name=user_profile.company_name)
            print(f"Seller: {seller}")
        except Seller.DoesNotExist:
            messages.error(request, "Seller not found.")
            return redirect('home')
        
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                product.sellerProduct = seller
                product.save()
                messages.success(request, "Product added successfully.")
                return redirect('seller_dashboard')
        else:
            form = ProductForm()
        return render(request, 'seller/add_product.html', {'form': form})

        
    
@login_required
def delete_product(request, pk):
   product = get_object_or_404(Product, pk=pk)
   user_profile = UserProfile.objects.get(user=request.user)
   try:
        seller = Seller.objects.get(name=user_profile.company_name)
        print(f"Seller: {seller}")
   except Seller.DoesNotExist:
            messages.error(request, "Seller not found.")
            return redirect('home')
   

   if product.sellerProduct == seller:  # Ensure the logged-in user owns the product
        product.delete()
        messages.success(request, "Product deleted successfully.")
   else:
        messages.error(request, "You do not have permission to delete this product.")
   return redirect('seller_dashboard')

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    user_profile = UserProfile.objects.get(user=request.user)
    
    try:
        seller = Seller.objects.get(name=user_profile.company_name)
    except Seller.DoesNotExist:
        messages.error(request, "Seller not found.")
        return redirect('home')
    
    # Ensure the logged-in user owns the product
    if product.sellerProduct != seller:
        messages.error(request, "You do not have permission to edit this product.")
        return redirect('seller_dashboard')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('seller_dashboard')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'seller/edit_product.html', {'form': form, 'product': product})

@login_required
def view_orders(request):
    orders = PurchaseOrder.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/view_orders.html', {'orders': orders})

@login_required
def order_details(request, order_id):
    # Fetch the specific order for the logged-in user
    order = get_object_or_404(PurchaseOrder, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(porder=order)
    return render(request, 'orders/order_details.html', {'order': order, 'order_items': order_items})