from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from django.utils import timezone
from .models import Product, Category, Order, OrderItem
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def home(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'store/home.html', context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)
    categories = Category.objects.all()
    context = {
        'category': category,
        'products': products,
        'categories': categories
    }
    return render(request, 'store/home.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item quantity was updated.")
            return redirect('cart_summary')
        else:
            order.items.add(order_item)
            messages.info(request, "Item was added to your cart.")
            return redirect('cart_summary')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item was added to your cart.")
        return redirect('cart_summary')

@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__slug=product.slug).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order_item.delete()
            messages.info(request, "Item quantity was updated.")
            return redirect('cart_summary')
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect('product_detail', slug=slug)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect('product_detail', slug=slug)

@login_required
def remove_single_item_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__slug=product.slug).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "Item was removed from your cart.")
            return redirect('cart_summary')
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect('product_detail', slug=slug)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect('product_detail', slug=slug)

@login_required
def cart_summary(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        context = {
            'order': order
        }
        return render(request, 'store/cart.html', context)
    except Order.DoesNotExist:
        messages.warning(request, "You do not have an active order.")
        return redirect('/')

@login_required
def checkout(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
    except Order.DoesNotExist:
        messages.warning(request, "You do not have an active order.")
        return redirect('home')

    if request.method == 'POST':
        address = request.POST.get('shipping_address')
        if address:
            order.shipping_address = address
            order.ordered = True
            order.save()
            
            # Update ordered status of items
            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()
            
            messages.success(request, "Your order was successful!")
            return redirect('home')
        else:
            messages.warning(request, "Please fill in the shipping address.")
            return redirect('checkout')

    context = {
        'order': order
    }
    return render(request, 'store/checkout.html', context)
