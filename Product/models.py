from datetime import datetime

from Category.models import Category
from django.db import models


# Product Model
class Product(models.Model):
	product_name = models.CharField(max_length=100, blank=False)
	product_price_ngn = models.PositiveIntegerField(blank=False)
	product_description = models.TextField(max_length=500, blank=True)
	category = models.ForeignKey(
		Category, on_delete=models.CASCADE, null=False, default=None)
	available_inventory = models.PositiveIntegerField(default=1)
	product_image = models.ImageField(
		upload_to='profile_pics', default='/home/emmanuel/Emmanuel/IT-Internship/user-avatar.png')
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.product_name
