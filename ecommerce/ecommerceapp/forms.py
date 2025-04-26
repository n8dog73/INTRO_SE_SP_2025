from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.db import models
from .models import UserProfile, Seller, Product, Category

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'state', 'city', 'zip_code']
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'placeholder': 'Address'}),
            'state': forms.TextInput(attrs={'placeholder': 'State'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'zip_code': forms.TextInput(attrs={'placeholder': 'Zip Code'}),
            #'groups': forms.Select(attrs={'placeholder': 'Select Group'}),
        }

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['name', 'website']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'manufacture', 'model_number', 'description', 'price', 'quantity', 'category', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Product Name'}),
            'manufacture': forms.TextInput(attrs={'placeholder': 'Manufacture'}),
            'model_number': forms.TextInput(attrs={'placeholder': 'Model Number'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Price'}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'Quantity'}),
            'category': forms.Select(attrs={'placeholder': 'Select Category'}),
            'image': forms.ClearableFileInput(attrs={'placeholder': 'Upload Image'}),
        }