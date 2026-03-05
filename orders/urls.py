from django.urls import path
from .views import CheckoutView, MidtransWebhookView

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('webhook/midtrans/', MidtransWebhookView.as_view(), name='midtrans-webhook'),
]