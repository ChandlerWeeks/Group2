from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from bigMoney.models import Seller
from bigMoney.models import Customer
from bigMoney.models import merchandise
from bigMoney.models import Order

admin.site.index_title = "Big Money"

"""
class CustomerInLine(admin.StackedInline):
    model = Customer
    can_delete = True
    verbose_name_plural = "Customer"

class SellerInLine(admin.StackedInline):
    model = Seller
    can_delete = True
    verbose_name_plural = "Seller"

class MerchandiseInLine(admin.StackedInline):
    model = merchandise
    can_delete = True
    verbose_name_plural = "merchandise"

class UserAdmin(admin.ModelAdmin):
    inlines = [MerchandiseInLine]
"""

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    fields = ['user','email','address','CompanyName','balance',
    'available_merch']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    fields = ['user','email','address','ShoppingCart','Orders']

@admin.register(merchandise)
class MerchandiseAdmin(admin.ModelAdmin):
    fields = ['title','cost','description','date_posted',
    'image', 'quantity_in_stock']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ['name', 'dateOrdered', 'Orders']