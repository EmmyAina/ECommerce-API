from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import CartItem,Cart
from .serializers import CartItemSerializer
class CartViewSet(ModelViewSet):
	my_tags = ['Cart']
	permission_classes = (IsAuthenticated,)
	serializer_class = CartItemSerializer

	def get_queryset(self):
		cart_id = Cart.objects.get(customer_id=self.request.user.id)
		return CartItem.objects.filter(cart_id=cart_id)
