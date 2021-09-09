from Account.serializers import UserSerializers
from .models import Cart, CartItem
from rest_framework import serializers
from Account.models import User
from Product.models import Product
from Cart.models import Cart
from Product.serializers import ProductSerializer

class CartSerializer(serializers.ModelSerializer):

	"""Serializer for the Cart model."""

	customer = UserSerializers(read_only=True)

	class Meta:
		model = Cart
		fields = (
			'id', 'customer', 'created_at', 'updated_at',
		)


class CartProductSerializer(serializers.ModelSerializer):

	class Meta:
		model = Product
		fields = (
			'product_name', 'product_price_ngn',
		)


class CartItemSerializer(serializers.ModelSerializer):

	"""Serializer for the CartItem model."""

	# cart = CartSerializer(read_only=True)
	# product = CartProductSerializer(read_only=True)

	class Meta:
		model = CartItem
		fields = (
			'id' ,'product', 'quantity',
		)

	def create(self, validated_data):

		validated_data['cart'] = Cart.objects.get(customer_id=self.context['request'].user)
		print(Cart.objects.get(customer_id=self.context['request'].user))
		cartItem_instance = self.Meta.model(**validated_data)
		cartItem_instance.save()
		return cartItem_instance
