from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import *
from .models import *

# Create your views here.
def home(request):
    #set what view to show, S, C, or unauthenticated
    show_seller_boxes = False
    show_customer_boxes = False
    show_unauthenticated_boxes = False
    if not request.user.is_authenticated:
        show_unauthenticated_boxes = True
    elif request.user.role == 'S':
        show_seller_boxes = True
    elif request.user.role == 'C':
        show_customer_boxes = True

    context = {
        'show_unauthenticated_boxes': show_unauthenticated_boxes,
        'show_seller_boxes': show_seller_boxes,
        'show_customer_boxes': show_customer_boxes
    } 
    return render(request, "home.html", context)

def loginview(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def change_address(request):
    address = request.user.address
    form = AddressForm(instance=address)
    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            request.user.address = address
            request.user.save()
            return redirect("home")

    return render(request, 'change_address.html', {'form': form})

@login_required
def view_account_details(request):
    user = request.user
    context = {
        'username': user.username,
        'name': user.name,
        'email': user.email,
        'balance': user.balance,
        'address': user.address, 
    }

    return render(request, "view_account_details.html", context)

@login_required
def edit_account(request):
    user = request.user
    if request.method == 'POST':
        form = accountDetailsForm(request.POST)
        if (form.is_valid()):
            user = form.save()
            return redirect('home')
    else:
        form = accountDetailsForm()

    return render(request, "edit_account.html", {"form": form})