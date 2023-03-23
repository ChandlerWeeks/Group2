from django.db import models
from django.contrib.auth.models import User

# Create your models here.


#DO NOT migrate models until model design is complete - thank you C:
"""
class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    CompanyName = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    balance = models.FloatField()
    address = models.ForeignKey(returnAddress, on_delete=models.CASCADE)
    

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    aaddress = models.ForeignKey(shippingAddress, on_delete=models.CASCADE)

class shoppingCart(models.Model):
    name = models.CharField(max_length=255)

class Order(models.Model):
    name = models.CharField(max_length=255)

class shippingAddress:
    RecipiantName = models.CharField(max_length=255)
    StreetAddress = models.CharField(max_length=255)
    City = models.CharField(max_length=255)
    State = models.charField(max_length=20)
    zipcode = models.intField()

    
class returnAddress:
    ShipperName = models.CharField(max_length=255)
    StreetAddress = models.CharField(max_length=255)
    City = models.CharField(max_length=255)
    State = models.charField(max_length=20)
    zipcode = models.intField()

class merchandise:
    name = models.CharField(max_length=255)

"""