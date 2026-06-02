from django.contrib import admin
from .models import Category, Product, OrderItem, Order

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'stock', 'is_active', 'category']
    list_filter = ['is_active', 'category']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(OrderItem)
admin.site.register(Order)
