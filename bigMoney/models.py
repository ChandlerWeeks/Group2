from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from django.core.validators import MinLengthValidator

# Create your models here.

class Address(models.Model):
    RecipiantName = models.CharField(max_length=255)
    StreetAddress = models.CharField(max_length=255)
    City = models.CharField(max_length=255)
    State = models.CharField(max_length=20)
    zipcode = models.IntegerField()

    #Note: pre allows the function to be interpreted by html
    def __str__(self):
        return f"""<pre>Name: {self.RecipiantName}
Street: {self.StreetAddress}
City: {self.City}
State: {self.State}
Zipcode: {self.zipcode}</pre>
        """
    


class merchandise(models.Model):
    poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    date_posted = models.DateTimeField(default=timezone.now)
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(max_length=1024)
    image = models.ImageField(default='default.jpg', upload_to='product_images')
    quantity_in_stock = models.IntegerField()
    quantity_sold = models.IntegerField(default=0)

    is_approved = models.BooleanField(default=None, null=True)

    GENRE_CHOICES = (
        ('clothing', 'Clothing'),
        ('books', 'Books'),
        ('movies', 'Movies'),
        ('computers', 'Computers'),
        ('food', 'Food'),
        ('cooking', 'Cooking'),
        ('outdoors', 'Outdoors'),
    )

    genre = models.CharField(max_length=255, choices=GENRE_CHOICES, null=True)

    def __str__(self):
        return f'{self.title} - {self.poster}'


class CartItem(models.Model):
    item = models.ForeignKey(merchandise, on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)

class shoppingCart(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    items = models.ManyToManyField(CartItem)

class Order(models.Model):
    date_ordered = models.DateTimeField(default=timezone.now)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    items = models.ManyToManyField(CartItem)

    def __str__(self):
        return f'Order made by {self.customer.username}'

class User(AbstractUser):
    USER_ROLES = (
        ("S", "Seller"),
        ("C", "Customer")
    )
    role = models.CharField(max_length=1, blank=False, choices=USER_ROLES, default="S")
    card_number = models.CharField(max_length=16, null=True, validators=[MinLengthValidator(16)])

    email = models.EmailField(max_length=255, default="")
    name = models.CharField(max_length=255, default="New User")
    balance = models.FloatField(default=0.0)

    #IMPORT THE FOLLOWING
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    

    # specific to seller, not accessible by customer
    available_merch = models.ManyToManyField(merchandise, default=None)

    # specific to customer, not accessible by seller
    ShoppingCart = models.ForeignKey(shoppingCart, on_delete=models.CASCADE, null=True)
    Orders = models.ManyToManyField(Order, default=None)

    is_approved = models.BooleanField(default=None, null=True)
    
    def __str__(self):
        return f'{self.username} ({self.role})'