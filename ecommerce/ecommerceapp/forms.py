from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.db import models
from .models import UserProfile, Seller

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'state', 'city', 'zip_code', 'groups']
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'placeholder': 'Address'}),
            'state': forms.TextInput(attrs={'placeholder': 'State'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'zip_code': forms.TextInput(attrs={'placeholder': 'Zip Code'}),
            'groups': forms.Select(attrs={'placeholder': 'Select Group'}),
        }

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['name', 'website']