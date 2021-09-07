import jwt
from Account.models import User
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .authentication import Authentication
from .models import TokenModel
from .serializers import LoginSerializers, RefreshTokenSerializers


class LoginView(GenericAPIView):
	permission_classes = (AllowAny,)

	my_tags = ['Auth']
	"""
	APIView for logging in user by checking the details provided and
	encoding the data with jwt then storing the encoded information
	in cookies.
	"""
	serializer_class = LoginSerializers

	def post(self, request):
		response, serializer = Response(), LoginSerializers(data=request.data)

		serializer.is_valid()
		user = User.objects.filter(email=serializer.data['email']).first()

		if user is None:
			response = Response(
						{'success': False,
						"error": "User not found", },
						status=status.HTTP_403_FORBIDDEN
					)
			return response

		if not user.check_password(serializer.data['password']):
			response = Response(
						{'success': False,
						"error": "Invalid Email or Password", },
						status=status.HTTP_403_FORBIDDEN
					)
			return response

		# if not user.verified:
		# 	response = Response(
        #             {'success': False,
        #              "error": "Please confirm your account with the otp before attempting to login", },
        #             status=status.HTTP_403_FORBIDDEN
        #         )
		# 	return response

		try:
			TokenModel.objects.filter(user_id=user.id).delete()
			payload = Authentication.create_token_for_user(user)

			refresh, access = payload['refresh'], payload['access']
			response.data = {
                            'success': True,
                            "message": "User Logged in",
                        				"access": payload['access'],
                        				"refresh": payload['refresh'],
                        }

			TokenModel.objects.create(
				user_id=user.id, refresh_token=refresh, access_token=access)
		except AttributeError:
			raise AuthenticationFailed()

		return response


class RefreshTokenView(GenericAPIView):
	my_tags = ['Auth']
	serializer_class = RefreshTokenSerializers
	permission_classes = (AllowAny,)

	def post(self, request):
		# Collect user refresh token
		serializer = RefreshTokenSerializers(data=request.data)
		serializer.is_valid(raise_exception=True)

		# Check if the refresh token is present in the token table
		try:
			current_token = TokenModel.objects.get(
				refresh_token=serializer.data['refresh_token'])
		except TokenModel.DoesNotExist:
			# raise Response({'message':'Refresh token is inalid'}, status=400)
			raise AuthenticationFailed('Refresh token invalid/expired')

		# Get the ID of user that is trying to refresh their token
		decoded_id = Authentication.decode_user_token(current_token.refresh_token)

		# Returns none if token is expired/invald; decoded_id=None
		if not decoded_id:
			return Response({'message': 'Token invalid/expired'}, status=400)

		current_user = User.objects.filter(id=decoded_id).first()

		renewed_tokens = Authentication.create_token_for_user(current_user)

		ref = renewed_tokens['refresh']
		acc = renewed_tokens['access']

		# Insert renewed refresh and access token to the current token model
		current_token.refresh_token = ref
		current_token.access_token = acc
		current_token.save()

		return Response({
			"refresh": ref,
			'access': acc,
		})
