from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from decouple import config
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from Account.models import User


class Authentication(BaseAuthentication):

	def authenticate(self, request):
		active_token = self.get_active_token(request.headers)
		decoded_id = self.decode_user_token(active_token)

		if not decoded_id:
			raise AuthenticationFailed('Token invalid or expired')

		return self.get_user(decoded_id), None

	@staticmethod
	def get_user(self, user_id):
		try:
			user = User.objects.get(id=user_id)
			return user.email
		except User.DoesNotExist:
			raise AuthenticationFailed('Cannot authenticate a user that doesnt exist')

	def get_active_token(self, headers):
		authorization = headers.get('Authorization', None)
		if authorization is None:
			raise AuthenticationFailed('Authorization token not provided')
		active_token = headers['Authorization'][7:]
		return active_token

	@staticmethod
	def decode_user_token(token):
		if not token:
			raise AuthenticationFailed('No User Logged in')
		try:
			payload = jwt.decode(token, config("ECOMM_SECRETKEY"), algorithms="HS256")
		except jwt.ExpiredSignatureError:
			# return None
			raise AuthenticationFailed('Session expired, Login or renew your token')

		current_user_id = payload['user_id']

		return current_user_id

	@staticmethod
	def create_token_for_user(user):
		refresh = RefreshToken.for_user(user)
		payload = {
			'user_id': user.id,
			'refresh': str(refresh),
			'access': str(refresh.access_token),
		}

		return payload
