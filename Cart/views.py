from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .models import CartItem,Cart
from .serializers import CartItemSerializer
from Product.models import Product
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from Utils.utils import get_actual_total

class CartViewSet(ModelViewSet):
	my_tags = ['Cart']
	permission_classes = (IsAuthenticated,)
	serializer_class = CartItemSerializer

	def get_queryset(self):
		cart_id = Cart.objects.get(customer_id=self.request.user.id)
		user_cart = CartItem.objects.filter(cart_id=cart_id)
		sub_total = get_actual_total(user_cart)
		print(sub_total)

		cart_id.total = sub_total
		cart_id.save()

		return CartItem.objects.filter(cart_id=cart_id)
