import os
import hashlib
import midtransclient
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import transaction
from .models import Product, Order, OrderItem
from .serializers import CheckoutSerializer

snap = midtransclient.Snap(
    is_production=os.getenv("MIDTRANS_IS_PRODUCTION", "False") == "True",
    server_key=os.getenv("MIDTRANS_SERVER_KEY"),
    client_key=os.getenv("MIDTRANS_CLIENT_KEY")
)

class CheckoutView(views.APIView):
    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        items_data = serializer.validated_data['items']
        
        try:
            with transaction.atomic():
                order = Order.objects.create()
                total_amount = 0
                
                for item in items_data:
                    product = Product.objects.select_for_update().get(id=item['product_id'])
                    
                    if product.stock < item['quantity']:
                        raise ValueError(f"Insufficient stock for {product.name}")
                    
                    product.stock -= item['quantity']
                    product.save()
                    
                    subtotal = product.price * item['quantity']
                    total_amount += subtotal
                    
                    OrderItem.objects.create(
                        order=order, product=product, 
                        quantity=item['quantity'], price_at_checkout=product.price
                    )
                
                order.total_price = total_amount
                order.save()
                
                param = {
                    "transaction_details": {
                        "order_id": str(order.order_id),
                        "gross_amount": float(total_amount)
                    }
                }
                
                midtrans_txn = snap.create_transaction(param)
                order.payment_url = midtrans_txn['redirect_url']
                order.save()
                
                return Response({"order_id": order.order_id, "payment_url": order.payment_url}, status=status.HTTP_201_CREATED)
                
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MidtransWebhookView(views.APIView):
    permission_classes = [] 
    
    def post(self, request):
        payload = request.data
        order_id = payload.get('order_id')
        status_code = payload.get('status_code')
        gross_amount = payload.get('gross_amount')
        signature_key = payload.get('signature_key')
        transaction_status = payload.get('transaction_status')
        
        server_key = os.getenv("MIDTRANS_SERVER_KEY")
        signature_data = f"{order_id}{status_code}{gross_amount}{server_key}"
        expected_signature = hashlib.sha512(signature_data.encode('utf-8')).hexdigest()
        
        if expected_signature != signature_key:
            return Response({"error": "Invalid signature"}, status=status.HTTP_403_FORBIDDEN)
            
        try:
            with transaction.atomic():
                order = Order.objects.select_for_update().get(order_id=order_id)
                
                if order.status in ['settlement', 'cancel', 'expire']:
                    return Response({"message": "Already processed"}, status=status.HTTP_200_OK)
                
                if transaction_status in ['capture', 'settlement']:
                    order.status = 'settlement'
                elif transaction_status in ['cancel', 'deny', 'expire']:
                    order.status = transaction_status
                        
                order.save()
            return Response({"message": "OK"}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    data = [
        {
            "id": p.id, 
            "name": p.name, 
            "price": p.price, 
            "stock": p.stock
        } for p in products
    ]
    return Response(data, status=status.HTTP_200_OK)