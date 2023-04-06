from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
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

def is_not_customer(user):
    return user.is_authenticated and user.role != 'C'

def is_not_seller(user):
    return user.is_authenticated and user.role != 'S'

@user_passes_test(is_not_customer) # makes sure user is not a customer, but a seller
@login_required
def create_listing(request):
    if request.method == 'POST':
        form = merchandiseForm(request.POST, request.FILES)
        if form.is_valid():
            merchandise_item = form.save(commit=False)
            merchandise_item.poster = request.user
            merchandise_item.save()
            request.user.available_merch.add(merchandise_item)
            return redirect('home')
    else:
        form = merchandiseForm()
    return render(request, 'create_listing.html', {'form': form})

def view_merchandise(request, item_id):
    item = get_object_or_404(merchandise, pk=item_id)
    return render(request, 'view_item.html', {'item': item})