from rest_framework import serializers
from .google_helper import Google
from .register import register_social_user
from decouple import config
from rest_framework.exceptions import AuthenticationFailed

class GoogleAuthSerializers(serializers.Serializer):
	auth_token = serializers.CharField()

	def validate_auth_token(self, auth_token):
		user_data = Google.validate(auth_token)
		try:
			user_data['sub']
		except:
			raise serializers.ValidationError(
				"Invalid or expired token, please try again"
			)
		# if user_data['aud'] != config('GOOGLE_CLIENT_ID'):
		# 	raise AuthenticationFailed("This request was not made from the platform, please contact admin")

		user_id = user_data['sub']
		email = user_data['email']
		name = user_data['name']
		provider = 'google'

		return register_social_user(
			provider, email, user_id, name
		)
