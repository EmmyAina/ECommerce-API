from .models import Product
from rest_framework import serializers
from Category.serializers import CategorySerializer

class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = '__all__'