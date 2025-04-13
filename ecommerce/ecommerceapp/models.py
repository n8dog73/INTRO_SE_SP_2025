from django.db import models
import os

def product_image_upload_path(instance, filename):
    # Ensures images are always uploaded to the 'products/' folder
    return os.path.join('products', filename)

class Product(models.Model):
    name = models.CharField(max_length=255)
    manufacture = models.CharField(max_length=255)
    model_number = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=50)
    image = models.ImageField(upload_to=product_image_upload_path)
    sellerProduct = models.CharField(max_length=255)

class Seller(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
