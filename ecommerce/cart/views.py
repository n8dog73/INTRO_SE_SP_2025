from django.shortcuts import render
from django.urls import path
from . import views


# Create your views here.
def cart_summary(request):
    # Logic to retrieve cart items and total price
    cart_items = request.session.get('cart', [])
    total_price = sum(item['price'] for item in cart_items)
    return render(request, 'cart/cart_summary.html', {'cart_items': cart_items, 'total_price': total_price})

def add_to_cart(request):
    # Logic to add item to cart
    product_id = request.POST.get('product_id')
    product_price = float(request.POST.get('product_price'))
    cart = request.session.get('cart', [])
    
    # Check if the product is already in the cart
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] += 1
            break
    else:
        cart.append({'id': product_id, 'price': product_price, 'quantity': 1})
    
    request.session['cart'] = cart
    return render(request, 'cart/cart_summary.html', {'cart_items': cart})

def remove_from_cart(request):
    # Logic to remove item from cart
    product_id = request.POST.get('product_id')
    cart = request.session.get('cart', [])
    
    # Remove the item from the cart
    cart = [item for item in cart if item['id'] != product_id]
    
    request.session['cart'] = cart
    return render(request, 'cart/cart_summary.html', {'cart_items': cart})

def update_cart(request):
    # Logic to update item quantity in cart
    product_id = request.POST.get('product_id')
    new_quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', [])
    
    # Update the item quantity
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] = new_quantity
            break
    
    request.session['cart'] = cart
    return render(request, 'cart/cart_summary.html', {'cart_items': cart})

def checkout(request):  
    # Logic to handle checkout process
    cart = request.session.get('cart', [])
    total_price = sum(item['price'] * item['quantity'] for item in cart)
    
    # Here you would typically handle payment processing and order creation
    return render(request, 'cart/checkout.html', {'cart_items': cart, 'total_price': total_price})

def checkout_success(request):
    # Logic to handle successful checkout
    cart = request.session.get('cart', [])
    
    # Clear the cart after successful checkout
    request.session['cart'] = []
    
    return render(request, 'cart/checkout_success.html', {'cart_items': cart})