from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import CartItem,Cart
from .serializers import CartItemSerializer
class CartViewSet(ModelViewSet):
	my_tags = ['Cart']
	permission_classes = (IsAuthenticated,)
	serializer_class = CartItemSerializer
	queryset = CartItem.objects.all()

	def get_queryset(self):
		cart= Cart.objects.get(customer_id=self.request.user.id)
		return self.queryset.filter(cart_id=cart)
