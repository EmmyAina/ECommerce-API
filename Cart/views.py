from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import CartItem,Cart
from .serializers import CartItemSerializer
class CartViewSet(ModelViewSet):
	"""
	This viewset automatically provides 'list', 'create', 'retrieve', 'update', and 'destroy' actions for user cart

	Viewset for User Cart endpoint
	"""
	my_tags = ['Cart']
	permission_classes = (IsAuthenticated,)
	serializer_class = CartItemSerializer
	queryset = CartItem.objects.all()

	def get_queryset(self):
		return self.queryset.filter(cart=Cart.objects.get(id=self.request.user))
