from rest_framework import serializers
from .models import Product, Order, OrderItem

class OrderItemInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class CheckoutSerializer(serializers.Serializer):
    items = OrderItemInputSerializer(many=True)