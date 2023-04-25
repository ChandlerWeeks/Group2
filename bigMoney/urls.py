from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
 path("", views.home, name="home"),
 path("register/", views.register_view, name="register"),
 path("login/", views.loginview, name="login"),
 path("logout/", views.logout_view, name="logout"),
 path("view_account/", views.view_account_details, name="view-account"),
 path('change_address/', views.change_address, name="change-address"),
 path('edit-account/', views.edit_account, name="edit-account"),
 path('create-listing/', views.create_listing, name="create-listing"),
 path('view-my-listings/', views.view_my_merchandise, name="view-my-listings"),
 path('view-my-sales/', views.view_my_sales, name='view-my-sales'),
 path('view-product/<int:item_id>/', views.view_merchandise, name="view-product"),
 path('redeem-funds/', views.redeem_funds, name="redeem_funds"),
 path('add_to_cart/<int:item_id>/', views.add_to_cart, name="add_to_cart"),
 path('view-cart/', views.view_cart, name="view-cart"),
 path('checkout/', views.checkout, name='checkout'),
 path('search/', views.search, name='search'),
 path('view-orders/', views.view_orders, name='view-orders'),
 path('view-order/<int:order_id>', views.view_order, name='view-order'),
 path('return-order/<int:order_id>', views.return_order, name='return-order' )
]

# allows for images to be uploaded
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 