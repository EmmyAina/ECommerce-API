from .models import CheckedOutOrder,TrackCoupon

#---------------Helper / Utility Classes ---------------

class CheckoutHelper():
	@staticmethod	
	def perform_checkout(cart,coupon,sub_total,discounted_total):
		"""
		Collect and save necessary details when customer 
		is ready for final checkout
		"""
		CheckedOutOrder.objects.filter(cart_id=cart).delete()

		checked_out = CheckedOutOrder()
		checked_out.cart = cart
		checked_out.coupon_applied = coupon
		checked_out.sub_total = sub_total
		checked_out.discounted_total = discounted_total

		checked_out.save()

	@staticmethod
	def track_coupon_use(customer,coupon):
		"""
		Store a used coupon with the customer that makes uses of
		it so it can be tracked
		"""
		save_used_coupon = TrackCoupon()
		save_used_coupon.customer = customer
		save_used_coupon.coupon = coupon

		save_used_coupon.save()


class AmountCalculationHelper():

	def get_actual_total(user_cart):
		"""
		Calculate the sub total of items in a user cart
		"""
		items_total = []
		for item in user_cart:
			items_total.append(item.product_total())
		sub_total = sum(items_total)

		return sub_total


	def get_discount_total(discount_percent, sub_total):
		"""
		Calculate the discounted total of items in a user cart
		"""
		discount_value = (discount_percent/100) * sub_total

		discount_total = sub_total - discount_value
		return discount_total



