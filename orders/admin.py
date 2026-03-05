from django.contrib import admin
from .models import Product, Order, OrderItem

# This tells Django to display the Product model and show these specific columns
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')

# This displays the Orders
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'status', 'total_price', 'created_at')
    readonly_fields = ('order_id',) # Prevents accidental editing of the unique ID

# This displays the individual items inside an order
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price_at_checkout')