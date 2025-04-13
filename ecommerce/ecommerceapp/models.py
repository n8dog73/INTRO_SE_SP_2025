from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
import os

def product_image_upload_path(instance, filename):
    # Ensures images are always uploaded to the 'products/' folder
    return os.path.join('products', filename)

class Seller(models.Model):
    name = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    manufacture = models.CharField(max_length=255)
    model_number = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_image_upload_path)
    sellerProduct = models.ForeignKey(Seller, on_delete=models.CASCADE )
   
    def __str__(self):
        return self.name



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    groups = models.OneToOneField(Group, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    company_name = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            user_profile = UserProfile(user=instance)
            user_profile.save()
    # Connect the signal to create a UserProfile when a User is created
    post_save.connect(create_user_profile, sender=User)
