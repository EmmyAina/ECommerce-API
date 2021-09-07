from .models import Product
from rest_framework.viewsets import ModelViewSet
from .serializers import ProductSerializer
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import FormParser, MultiPartParser
from core.custompermissions import IsAdminOrReadOnly

class ProductViewSet(ModelViewSet):
	my_tags = ['Product']
	permission_classes = (IsAdminOrReadOnly,)
	# parser_classes = (FormParser, MultiPartParser)

	queryset = Product.objects.all()
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ('product_name', 'product_description')
	serializer_class = ProductSerializer
