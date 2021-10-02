from rest_framework.generics import GenericAPIView
from .serializers import GoogleAuthSerializers
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class GoogleSocialAuthView(GenericAPIView):
	serializer_class = GoogleAuthSerializers

	def post(self, request):
		"""
		Pass in an authentication token, and retrieve the user Information
		"""

		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)

		data = ((serializer.validated_data)['auth_token'])

		return Response(data, status=status.HTTP_200_OK)
