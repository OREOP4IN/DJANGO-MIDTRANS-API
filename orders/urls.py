from django.urls import path
from . import views
from .views import CheckoutView, MidtransWebhookView

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('webhook/midtrans/', MidtransWebhookView.as_view(), name='midtrans-webhook'),
    path('products/', views.product_list, name='product-list'),
]