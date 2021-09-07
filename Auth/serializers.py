from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import ugettext_lazy as _
import jwt
from decouple import config


class LoginSerializers(serializers.Serializer):
	email = serializers.CharField(max_length=255)
	password = serializers.CharField(
		label=_("Password"),
		style={'input_type': 'password'},
		trim_whitespace=False,
		max_length=128,
		write_only=False
	)


class OTPSerializers(serializers.Serializer):
	otp = serializers.CharField(max_length=6)


class RefreshTokenSerializers(serializers.Serializer):
	refresh_token = serializers.CharField(max_length=500)
