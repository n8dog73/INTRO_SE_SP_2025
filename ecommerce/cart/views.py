from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from ecommerceapp.models import Product, PurchaseOrder, OrderItem, Seller
from django.contrib import messages
from django.db import transaction
from . import views


# Create your views here.
def cart_summary(request):
    # Logic to retrieve cart items and total price
    cart = request.session.get('cart', [])
    print(f"Cart Contents: {cart}")  # Debugging: Print the cart contents
    #cart_items = request.session.get('cart', [])
    #total_price = sum(item['price'] for item in cart)
    total_price = sum(item['price'] * item['quantity'] for item in cart)
    print(f"Product: {cart}")  # Debugging: Print the total price
    return render(request, 'cart/cart_summary.html', {'cart_items': cart, 'total_price': total_price})


def add_to_cart(request, product_id):
    # Logic to add item to cart
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')
    print(f"Product ID: {product_id}")
    from ecommerceapp.models import Product
    try:
        product = Product.objects.get(id=product_id)
        product_name = product.name #Product.objects.get(id=product_id).name
        product_price = float(product.price)
    except Product.DoesNotExist:
        return redirect('cart_summary')
    
    print(f"Product Price: {product_price}")
    
    cart = request.session.get('cart', [])
    # Check if the product is already in the cart
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] += 1
            break
    else:
        cart.append({'id': product_id, 'product':product_name,'price': product_price, 'quantity': 1})
    
    request.session['cart'] = cart
    print(cart)
    return redirect('cart_summary')  # Redirect to cart summary page
    #return render(request, 'cart/cart_summary.html', {'cart_items': cart})

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
    if not cart:
        return redirect('cart_summary')

    # Create an order
    order = PurchaseOrder.objects.create(user=request.user)
    total_price = 0

    for item in cart:
        product = Product.objects.get(id=item['id'])
        
          # Ensure the product has a valid sellerProduct
        if not product.sellerProduct:
            default_seller = Seller.objects.first()
            if default_seller:
                product.sellerProduct = default_seller
                product.save()
            else:
                return redirect('cart_summary')  # Handle the case where no default seller exists
        
        quantity = item['quantity']
        price = product.price * quantity
        total_price += price

        # Create an OrderItem
        OrderItem.objects.create(porder=order, product=product, quantity=quantity, price=price, sellerProduct=product.sellerProduct)
        # Check if the product is available in stock
        if product.quantity < quantity:
            messages.error(request, f"Not enough stock for {product.name}.")
            return redirect('cart_summary')

        # Reduce product quantity
        product.quantity -= quantity
        product.save()

    # Update the total price of the order
    order.total_price = total_price
    order.save()

    # Clear the cart
    request.session['cart'] = []
    print(f"Order Retrieved: ID={order.id}, Total Price={order.total_price}")  # Debugging
    return render(request, 'cart/payment_page.html', {'order': order})
    #cart = request.session.get('cart', [])
    #total_price = sum(item['price'] * item['quantity'] for item in cart)
    
    # Here you would typically handle payment processing and order creation
    #return render(request, 'cart/checkout.html', {'cart_items': cart, 'total_price': total_price})

def checkout_success(request, order_id):
    try:
        order = PurchaseOrder.objects.get(id=order_id, user=request.user)
    except PurchaseOrder.DoesNotExist:
        return redirect('cart_summary')
    user_profile = request.user.userprofile

    # Calculate the total price of the order
    total_price = sum(item.price * item.quantity for item in order.items.all())

    if user_profile.cashamount < total_price:
        order.delete()  # Delete the order if insufficient funds
        messages.error(request, "Insufficient funds in your account to complete the purchase.")
        return redirect('cart_summary')  # Redirect back to the cart if insufficient funds

    # Check if the user has enough cashamount
    if user_profile.cashamount >= total_price:
        # Deduct the total price from the user's cashamount
        user_profile.cashamount -= total_price
        user_profile.save()

        item_details = []
        for item in order.items.all():
            seller = item.product.sellerProduct
            amount = item.price * item.quantity
            seller.cashamount += amount
            seller.save()


            item_details.append({
                'seller': seller.name,
                'amount': amount
            })

        # Update the order status to 'Completed'
        order.payment_status = 'Completed'
        order.save()

        messages.success(request, "Purchase successful! Your account has been charged.")
    else:
        messages.error(request, "Insufficient funds in your account to complete the purchase.")
        return redirect('cart_summary')  # Redirect back to the cart if insufficient funds
    
    #items_details = [
    #    {'seller':item.product.sellerProduct.name,
    #     'amount':item.price * item.quantity
    #     }
    #     for item in order.items.all()
    #]
    print(f"Item Details: {item_details}")  # Debugging
    return render(request, 'cart/checkout_success.html', {'order': order, 'remaining_cash': user_profile.cashamount,'item_details': item_details})
    
   

def clear_cart(request):
    request.session['cart'] = []
    return redirect('cart_summary')

def payment_page(request, order_id):
    try:
        order = PurchaseOrder.objects.get(id=order_id, user=request.user)
        print(f"Order Retrieved: ID={order.id}, Total Price={order.total_price}")  # Debugging
    except PurchaseOrder.DoesNotExist:
        return redirect('cart_summary')

    if request.method == 'POST':
        # Log payment information
        payment_method = request.POST.get('payment_method', 'Credit Card')
        transaction_id = request.POST.get('transaction_id', '123456789')  # Simulated transaction ID
        order.payment_method = payment_method
        order.payment_status = 'Completed'
        order.transaction_id = transaction_id
        order.save()

        return redirect('checkout-success', order_id=order.id)

    return render(request, 'cart/payment_page.html', {'order': order})