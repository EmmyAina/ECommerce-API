from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from Cart.models import Cart
from .serializers import OrderItemSerializer
from rest_framework import generics

class CheckoutCart(generics.CreateAPIView):
	my_tags = ['Checkout']
	permission_classes = (IsAuthenticated, )
	serializer_class = OrderItemSerializer

	def post(self,request):
		current_cart = Cart.objects.filter(owner=request.user.id)
		print(current_cart)
		coupon_code = request.data['coupon_code']
		pass

	def get(self,request):
		current_cart = Cart.objects.filter(owner=request.user.id)
		print(current_cart)
		coupon_code = request.data['coupon_code']
		pass
