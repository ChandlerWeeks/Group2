"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


# Cannot be used until models are completed

from bigMoney.models import Seller
from bigMoney.models import Cusomter


# Register your models here.
class SellerInLine(admin.StackedInline):
    model = Seller
    can_delete = True
    verbose_name_plural = "Seller"

class CustomerInLine(admin.StackedInline):
    model = Cusomter
    can_delete = True
    verbose_name_plural = "Customer"

class UserAdmin(BaseUserAdmin):
    inlines = (SellerInLine,)
"""