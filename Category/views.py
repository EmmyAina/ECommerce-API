# from Product.models import Product
# from Product.serializers import Producterializer
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .models import Category
from .serializers import CategorySerializer

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response


class CategoryViewSet(ModelViewSet):
	my_tags = ['Category']
	# permission_classes = (IsAdminUser,)
	queryset = Category.objects.all()
	search_fields = ['category_name', ]
	filter_backends = [SearchFilter, OrderingFilter]
	serializer_class = CategorySerializer


# class ProductinCategoryView(APIView):

# 	"""
# 	APIView for retrieving a list of Products that belongs to a Category
# 	by the category id.
# 	Operation can be carried out any user.
# 	"""
# 	my_tags = ['Category']
# 	permission_classes = (AllowAny,)

# 	def get(self, request, id):
# 		Product = Product.objects.filter(category=id)

# 		ser = Producterializer(Product, many=True)

# 		return Response(ser.data)
