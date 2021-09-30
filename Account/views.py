from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.parsers import FormParser, MultiPartParser
from Account.models import User, UserBio
from Account.serializers import (UserBioSerializers,UserSerializers)
import jwt
from rest_framework_simplejwt.tokens import RefreshToken
from core.tasks import Tasks
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from decouple import config
class RegisterView(GenericAPIView):
	"""
	Endpoint for Registering a new user
	
	#
	"""
	my_tags = ['User']
	permission_classes = (AllowAny,)
	serializer_class = UserSerializers
	parser_classes = (FormParser, MultiPartParser)

	def post(self, request):
		response = Response()
		serialized_data = UserSerializers(data=request.data)
		serialized_data.is_valid(raise_exception=True)
		serialized_data.save()
		
		# Verify Email
		user_data = serialized_data.data
		user = User.objects.get(email=user_data['email'])
		token = RefreshToken.for_user(user).access_token

		current_site = get_current_site(request).domain
		relative_link = reverse('email-verify')
		abs_url = f"http://{current_site}{relative_link}?token={str(token)}"
		email_body = f"Hi {user.username}, Use the link below to verify your email \n {abs_url}"
		data = {"body": email_body, "subject": 'Verify your email',
                    "recepient": [user.email], "sender": config("ECOMM_MAILGUNEMAIL")}
		Tasks.send_verification_mail.delay(data)


		response.data = {
			'success': True,
			'id': serialized_data.data['id'],
			'message': "Account created successfully. Check your mail to verify your account",
		}
		response.status = status.HTTP_201_CREATED
		
		return response

class VerifyEmail(GenericAPIView):
	"""
	Endpoint for verifying a new user's email address before login
	
	This endpoint send a verification link to the registered email address
	"""
	my_tags = ['User']

	def get(self, request):
		token = request.GET.get("token")
		response = Response()
		try:
			payload = jwt.decode(token, config("ECOMM_SECRETKEY"), algorithms=["HS256"])
			user = User.objects.get(id=payload['user_id'])
			if not user.verified:
				user.verified = True
				user.save()
				response.data = {
					"detail": "Account verified successfully. Please proceed to login"}
				response.status = status.HTTP_200_OK
				return response

		except jwt.ExpiredSignatureError as identifier:
			response.data = {"error": "Verification Token Expired. Please try again"}
			response.status = status.HTTP_400_BAD_REQUEST
			return response

		except jwt.DecodeError as identifier:
			response.data = {"error": "Invalid Verification Token. Please try again"}
			response.status = status.HTTP_400_BAD_REQUEST

			return response
class UserView(ReadOnlyModelViewSet):
	"""
	Endpoint for getting the current user's account details
	
	Operation can be carried out only logged in user.
	"""
	my_tags = ['User']
	permission_classes = (IsAuthenticated, )
	serializer_class = UserSerializers
	queryset = User.objects.all()

	def get_queryset(self):
		return self.queryset.filter(id=self.request.user.id)


class UpdateBioViewSet(ModelViewSet):
	my_tags = ['User-Profile']
	permission_classes = (IsAuthenticated,)
	parser_classes = (FormParser, MultiPartParser)
	serializer_class = UserBioSerializers

	def get_queryset(self):
		return UserBio.objects.filter(user=self.request.user)
