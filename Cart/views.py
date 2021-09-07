from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .models import CartItem,Cart
from .serializers import CartItemSerializer
from Product.models import Product
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed


class AddItemToCart(ModelViewSet):
	my_tags = ['Cart']
	permission_classes = (IsAuthenticated,)
	serializer_class = CartItemSerializer

	def get_queryset(self):
		cart_id = Cart.objects.get(customer_id=self.request.user.id)
		print(cart_id)
		return CartItem.objects.filter(cart_id=cart_id)
	"""
	APIView that takes a product id and adds it to the current user's cart,
	it collects the quantity of products that needs to be added to the cart
	"""

	def post(self, request):

		current_cart = Cart.objects.get(customer=request.user.id)
		print(request.user.id)
		try:
			product_to_add = Product.objects.get(id=request.data['product_id'])
		except Product.DoesNotExist:
			raise AuthenticationFailed("Product does not exist")
		add_item = CartItem(cart=current_cart,
                      product_id=request.data['product_id'], quantity=request.data['quantity'])
		serialized_item = CartItemSerializer(data=request.data)
		if serialized_item.is_valid():
			add_item.save()

		return Response(serialized_item.data)


