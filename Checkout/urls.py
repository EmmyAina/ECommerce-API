from django.urls import include, path
from rest_framework import routers
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('api/v1/cart/order',
         views.CheckoutCart.as_view(), name='order-from-cart'),
]
