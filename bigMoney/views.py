from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.cache import cache_control
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse
from .forms import *
from .models import *
from decimal import Decimal
from django.utils.decorators import method_decorator

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

# User can logout and click back to view pages, but pages are dummy pages when this is done
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
        'card_number': user.card_number
    }

    return render(request, "view_account_details.html", context)

@login_required
def edit_account(request):
    user = request.user
    if request.method == 'POST':
        form = accountDetailsForm(request.POST, instance=user)
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
    related_items = merchandise.objects.filter(genre=item.genre).exclude(pk=item_id)[:2]

    messages.get_messages(request) # retrieve any messages

    return render(request, 'view_item.html', {'item': item, 'related_items': related_items})

@login_required
def view_my_merchandise(request):
    listings = request.user.available_merch.all()
    context = {'listings': listings}
    return render(request, 'view_my_listings.html', context)

@login_required
def view_my_sales(request):
    message = request.GET.get('message')
    user = request.user
    context = {'user': user}
    if message:
        context['message'] = message
    return render(request, "view_my_sales.html", context)

@login_required
def redeem_funds(request):
    user = request.user
    user.balance = 0.0
    user.save()
    message = "Funds Recieved Successfully"
    return redirect(reverse('view-my-sales') + '?message=' + message)

@login_required
def add_to_cart(request, item_id):
    merch = get_object_or_404(merchandise, pk=item_id)
    if (merch.quantity_in_stock < 1):
        messages.error(request, "none available to purchase")
        return redirect('view-product', item_id=item_id)
    cart, created = shoppingCart.objects.get_or_create(customer=request.user)
    cart_items = cart.items.all()
    exists = False
    for cart_item_i in cart_items:
        if merch == cart_item_i.item:
            exists = True
            cart_item = cart_item_i
    if not exists:
        cart_item = CartItem.objects.create(item = merch)


    if exists:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1

    cart_item.save()
    cart.items.add(cart_item)

    messages.success(request, f'a {merch.title} has been added to your cart!')
    return redirect('view-product', item_id=item_id)

@login_required
def view_cart(request):
    user = request.user
    cart = shoppingCart.objects.get_or_create(customer=request.user)
    if cart[0].items != None:
        items = cart[0].items.all()
    else:
        items = None
    total_cost = 0

    for cart_item in items:
        total_cost += cart_item.item.cost * cart_item.quantity

    context = {'items': items, 'total_cost': total_cost}
    return render(request, "view_cart.html", context)

@login_required
def checkout(request):
    if request.method == 'POST':
        cart = shoppingCart.objects.get(customer=request.user)
        #total_cost = Decimal(str('0.0'))
        total_cost = 0

        if cart.items.count() == 0:
            messages.error(request, 'Please add an item to the cart')
            return redirect('view-cart')

        # Calculate total cost of items in the cart
        for cart_item in cart.items.all():
            total_cost += cart_item.item.cost * cart_item.quantity

        # Check if the user has enough balance to pay for the items
        if request.user.card_number == None:
            messages.error(request, 'Please add a card before making a purchase')
            return redirect('view-cart')

        print("TYPE", type(request.user.balance))

        # Update user's balance
        # unsupported operand type(s) for -=: 'float' and 'decimal.Decimal'
        #request.user.balance -= total_cost
        #request.user.save()

        # Update item quantity_in_stock and quantity_sold
        for cart_item in cart.items.all():
            item = cart_item.item
            item.quantity_in_stock -= cart_item.quantity
            item.quantity_sold += cart_item.quantity
            cart_item.item.poster.balance += float(cart_item.item.cost * cart_item.quantity)
            item.save()
            cart_item.item.poster.save()

        # Create the order
        order = Order.objects.create(customer=request.user)
        for item in cart.items.all():
            order.items.add(item)
        order.customer = request.user
        request.user.Orders.add(order)
        order.save()
        messages.success(request, 'Order successfully placed!')

        # Clear the shopping cart
        cart.items.clear()

        # Redirect to a success page or the home page
        return redirect('view-cart')

def search(request):
    query = request.GET.get('query')
    results = merchandise.objects.filter(title__icontains=query)
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'search_results.html', context)

@login_required
def view_orders(request):
    messages.get_messages(request) # retrieve any messages
    user = request.user
    orders = user.Orders.all()
    context = {"orders": orders}
    return render(request, "view_orders.html", context)

@login_required
def view_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    # calculate the total cost of the order
    total_cost = 0
    for item in order.items.all():
            total_cost += item.item.cost * item.quantity

    context = {"order": order, "cost": total_cost}

    return render(request, 'view_order.html', context)

@login_required
def return_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    for cartItem in order.items.all():
        cartItem.item.poster.balance -= float(cartItem.item.cost * cartItem.quantity)
        cartItem.item.poster.save()

    order.delete()

    messages.success(request, "Successfully Returned Order!")
    return redirect('view-orders')