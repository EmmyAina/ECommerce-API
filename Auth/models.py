from django.db import models
from Account.models import User

# Create your models here.
class TokenModel(models.Model):
	user = models.OneToOneField(
		User, related_name='token_detail', on_delete=models.CASCADE)
	refresh_token = models.CharField(max_length=400)
	access_token = models.CharField(max_length=400)

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
