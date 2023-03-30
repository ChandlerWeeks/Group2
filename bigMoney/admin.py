from django.contrib import admin
from django.contrib.auth.models import User
from bigMoney.models import User, merchandise, Order

admin.site.index_title = "Big Money"

class MerchandiseInLine(admin.StackedInline):
    model = merchandise
    can_delete = True
    verbose_name_plural = "merchandise"

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ['username', 'name', 'email', 'role', 'address', 'balance', 'available_merch',
              'ShoppingCart', 'Orders'
              ]

@admin.register(merchandise)
class MerchandiseAdmin(admin.ModelAdmin):
    fields = ['title','cost','description','date_posted',
    'image', 'quantity_in_stock']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ['name', 'dateOrdered', 'Orders']