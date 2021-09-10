from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import FormParser, MultiPartParser
from Account.models import User, UserBio
from Account.serializers import (UserBioSerializers,
                                 UserSerializers)
from Cart.models import Cart

class RegisterView(GenericAPIView):
	my_tags = ['Auth']
	permission_classes = (AllowAny,)
	serializer_class = UserSerializers

	def post(self, request):
		response = Response()
		serialized_data = UserSerializers(data=request.data)
		serialized_data.is_valid(raise_exception=True)
		serialized_data.save()

		response.data = {
			'success': True,
			'id': serialized_data.data['id'],
			'message': "Account created successfully",
		}
		response.status = status.HTTP_201_CREATED
		
		return response

class UpdateBioViewSet(ModelViewSet):
	my_tags = ['User-Profile']
	permission_classes = (IsAuthenticated,)
	parser_classes = (FormParser, MultiPartParser)
	serializer_class = UserBioSerializers

	def get_queryset(self):
		return UserBio.objects.filter(user=self.request.user)
