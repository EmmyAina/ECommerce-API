from rest_framework import serializers
from .models import User, UserBio
from Cart.models import Cart


class UserBioSerializers(serializers.ModelSerializer):

	class Meta:
		model = UserBio
		exclude = ('user',)

	def create(self, validated_data):

		validated_data['user'] = self.context['request'].user
		profile_instance = self.Meta.model(**validated_data)
		profile_instance.save()
		return profile_instance


class UserSerializers(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'email', 'username', 'gender', 'password', 'profile_picture' ]
		extra_kwargs = {'password': {'write_only': True}}

	def create(self, validated_data):
		password = validated_data.pop('password', None)
		user_instance = self.Meta.model(**validated_data)

		if password != None:
			user_instance.set_password(password)
		user_instance.save()
		
		# Create a cart for the new user
		new_cart = Cart(id=user_instance)
		new_cart.save()
		return user_instance
