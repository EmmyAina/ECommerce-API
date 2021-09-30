from datetime import datetime, timedelta, timezone
from django.contrib.auth.models import AbstractBaseUser, Permission, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
import uuid
from .manager import UserManager

default_proile_pic = ['https://bit.ly/3xA57e3']

GENDER = (
	('Male', 'Male'),
	('Female', 'Female'),
	('Others', 'Others'),
)


class User(AbstractBaseUser, PermissionsMixin):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	email = models.EmailField(
		_('email address'), null=True, blank=True, unique=True)
	username = models.CharField(max_length=255,)
	password = models.CharField(max_length=255, null=True)
	gender = models.CharField(max_length=50, choices=GENDER, blank=True)
	is_staff = models.BooleanField(default=False)
	profile_picture = models.ImageField(
            upload_to='staticfiles', default='./staticfiles/user-avatar.png')
	date_joined = models.DateTimeField(auto_now_add=True, null=True)
	verified = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	class Meta:
		ordering = ('-date_joined',)

	objects = UserManager()

	def __str__(self):
		return self.email


class UserBio(models.Model):
	user = models.OneToOneField(
		User, on_delete=models.CASCADE, related_name='user_profile')
	date_of_birth = models.DateField(blank=True, null=True)
	country = models.CharField(max_length=30)
	state = models.CharField(max_length=30)
	city = models.CharField(max_length=30)
	address = models.CharField(max_length=70)

	def __str__(self):
		return f'{self.user.email} {self.state} {self.date_of_birth}'
	class Meta:
		verbose_name_plural = 'User Info'
