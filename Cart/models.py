from django.db import models
from Account.models import User
from Product.models import Product
from django.conf import settings


class Cart(models.Model):
	customer = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		related_name='cart',
		on_delete=models.CASCADE,
	)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.customer.email}'


class CartItem(models.Model):

	product = models.ForeignKey(
		Product,
		related_name='cartItem',
		on_delete=models.CASCADE,
	)

	cart = models.ForeignKey(
		Cart,
		on_delete=models.CASCADE,
		related_name='cartItem',
		null=True,
		blank=True,
	)

	quantity = models.PositiveIntegerField(default=1, null=True, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.product.product_name} {self.cart.customer.email}'


# # Create your models here.
# class Cart(models.Model):
# 	quantity = models.IntegerField(blank=False)
# 	owner = models.ForeignKey(User, on_delete=models.CASCADE)
# 	product = models.ForeignKey(Product, on_delete=models.CASCADE)
# 	time_updated = models.DateTimeField(auto_now_add=True)

# 	def __str__(self):
# 		return f'{self.owner.username} {self.product.product_name}'

# 	def product_total(self):
# 		product_total = self.product.product_price_ngn * self.quantity
# 		return product_total

# 	def sub_total(self):
# 		total_products = len(self)
# 		items = 0
# 		sub_total = []
# 		while items != total_products:
# 			sub_total.append(self.product_total)
# 			items+=1
		
# 		return sub_total
		

