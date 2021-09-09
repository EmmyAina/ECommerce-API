from django.db.models.fields.related import ForeignKey
from Cart.serializers import CartProductSerializer
from Cart.models import Cart
from django.db import models
import uuid
from Account.models import User

class Coupon(models.Model):
	code = models.CharField(max_length=7, unique=True)
	value = models.IntegerField()
	description = models.CharField(max_length=100)
	active = models.BooleanField(default=True)
	num_available = models.IntegerField(default=1)
	num_used = models.IntegerField(default=0)
	one_time_use = models.BooleanField(default=True)
	date_added = models.DateTimeField(auto_now=True)
	expiry_date = models.DateTimeField()

	def __str__(self):
		return self.code
	
	def is_usable(self):
		is_active = True

		if self.active == False:
			is_active = False
		if self.num_used >= self.num_available and self.num_available != 0:
			is_active = False

		return is_active

	def use_coupon(self):
		self.num_used += 1
		if self.num_used >= self.num_available:
			self.active = False
		
		self.save()

	def has_been_redeemed(self,user):
		been_redeemed = False
		tracked_coupons = TrackCoupon.objects.filter(customer=user)
		used_codes = []
		for tracled_coupon in tracked_coupons:
			used_codes.append(tracled_coupon.coupon.code)
		if self.code in used_codes:
			been_redeemed = True
		return been_redeemed
class CheckedOutOrder(models.Model):
	purchase_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
	coupon_applied = models.ForeignKey(Coupon, on_delete=models.CASCADE, default=None, blank=True, null=True)
	sub_total = models.DecimalField(max_digits=10, decimal_places=2)
	discounted_total = models.DecimalField(max_digits=10, decimal_places=2)

	success = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.cart.customer.email} OrderPlaced: {self.success}'

class TrackCoupon(models.Model):
	customer = models.ForeignKey(User, on_delete=models.CASCADE)
	coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.customer.email}: {self.coupon.code}'
