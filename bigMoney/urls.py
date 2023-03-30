from django.urls import path
from . import views

urlpatterns = [
 path("", views.home, name="home"),
 path("register/", views.register_view, name="register"),
 path("login/", views.loginview, name="login"),
 path("logout/", views.logout_view, name="logout"),
 path('change_address', views.change_address, name="change-address")
]