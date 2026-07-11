from django.urls import path
from . import views

urlpatterns = [

    # Home
    path("", views.home, name="home"),

    # Static Pages
    path("about/", views.about, name="about"),
    path("news/", views.news, name="news"),
    path("support/", views.support, name="support"),

    # Authentication
    path("register/", views.register, name="register"),

    # Products
    path("product/<int:pk>/", views.product_detail, name="product_detail"),

    # Cart
    path("cart/", views.cart, name="cart"),
    path("cart/add/<int:pk>/", views.add_to_cart, name="add_to_cart"),

    # Checkout
    path("checkout/", views.checkout, name="checkout"),

    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
]