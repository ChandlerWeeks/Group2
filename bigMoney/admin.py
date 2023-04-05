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
    list_display = ['username', 'name', 'email', 'balance', 'address', 'is_approved']
    fields = ['is_approved']

@admin.register(merchandise)
class MerchandiseAdmin(admin.ModelAdmin):
    fields = ['title','cost','description','date_posted',
    'image', 'quantity_in_stock', "is_approved"]
    ordering = ('-date_posted',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ['date_ordered', 'Order']
    ordering = ('-date_ordered',)
