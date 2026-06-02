from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<slug:slug>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove-single-item/<slug:slug>/', views.remove_single_item_from_cart, name='remove_single_item'),
    path('cart/', views.cart_summary, name='cart_summary'),
    path('checkout/', views.checkout, name='checkout'),
    path('register/', views.register, name='register'),
]
