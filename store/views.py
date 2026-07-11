from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .models import Product, Cart, Order
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# ==========================
# Home Page
# ==========================

def home(request):
    products = Product.objects.all()

    return render(request, "store/home.html", {
        "products": products
    })


# ==========================
# About Page
# ==========================

def about(request):
    return render(request, "store/about.html")


# ==========================
# News Page
# ==========================

def news(request):
    return render(request, "store/news.html")


# ==========================
# Support Page
# ==========================

def support(request):
    return render(request, "store/support.html")


# ==========================
# Product Details
# ==========================

def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)

    return render(request, "store/product_detail.html", {
        "product": product
    })


# ==========================
# Add to Cart
# ==========================

@login_required
def add_to_cart(request, pk):

    product = get_object_or_404(Product, id=pk)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1

    cart_item.save()

    return redirect("cart")


# ==========================
# Shopping Cart
# ==========================

@login_required
def cart(request):

    items = Cart.objects.filter(user=request.user)

    total = sum(
        item.product.price * item.quantity
        for item in items
    )

    return render(request, "store/cart.html", {
        "items": items,
        "total": total
    })


# ==========================
# Checkout
# ==========================

@login_required
def checkout(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    if cart_items.exists():

        Order.objects.create(
            user=request.user,
            total_amount=total
        )

        cart_items.delete()

    return render(request, "store/checkout.html", {
        "total": total
    })


# ==========================
# User Registration
# ==========================

def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect("home")

    else:

        form = RegisterForm()

    return render(request, "store/register.html", {
        "form": form
    })

# ==========================
# Login
# ==========================

def user_login(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("home")

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(request, "store/login.html")


# ==========================
# Logout
# ==========================

@login_required
def user_logout(request):

    logout(request)

    return redirect("home")