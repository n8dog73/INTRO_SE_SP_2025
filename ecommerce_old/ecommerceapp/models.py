from django.db import models

class users(models.Model):
    useremail = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    useraddress = models.CharField(max_length=255)
    userCity = models.CharField(max_length=255)
    userState = models.CharField(max_length=255)
    userZipCode = models.PositiveIntegerField
    userPhoneNumber = models.PositiveIntegerField(max_length=8)
    

