# Create your views here.
from django.db import models

# Category Model
class Category(models.Model):
	category_name = models.CharField(max_length=100, blank=False)

	def __str__(self):
		return self.category_name

	class Meta:
		verbose_name_plural = 'Categories'
		ordering = ['-category_name']
