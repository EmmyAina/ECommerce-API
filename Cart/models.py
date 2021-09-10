from django.db import models
from Account.models import User
from Product.models import Product
from django.conf import settings


class Cart(models.Model):
	id = models.OneToOneField(
		settings.AUTH_USER_MODEL, related_name='cart', on_delete=models.CASCADE, primary_key=True,)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f'{self.id.email}'


class CartItem(models.Model):

	product = models.ForeignKey(Product,related_name='cartItem', on_delete=models.CASCADE)
	cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cartItem',null=True,blank=True)
	quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
	added_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True)

	class Meta:
		ordering = ['-added_at']

	def __str__(self):
		return f'{self.product.product_name} {self.cart.id.email}'
	
	def product_total(self):
		product_total = self.product.product_price_ngn * self.quantity
		return product_total
