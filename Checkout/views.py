from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from Cart.models import Cart
from .serializers import ApplyCouponSerializer, CouponSerializer,PaymentDetailSerializer
from rest_framework import generics
from .stripe_api import StripePaymentGateway
from rest_framework.exceptions import AuthenticationFailed
from Cart.models import Cart, CartItem
from Cart.serializers import CartItemSerializer
from Checkout.models import Coupon, CheckedOutOrder
from .helper import AmountCalculationHelper, CheckoutHelper

class CheckoutCartItems(generics.ListAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = ApplyCouponSerializer
	my_tags = ['Checkout']

	def get_queryset(self):
		cart = Cart.objects.get(customer_id=self.request.user.id)
		return CartItem.objects.filter(cart_id=cart)

	def get(self, request):

		response = Response()
		response.data = {}

		cart = Cart.objects.get(customer_id=self.request.user.id)
		user_cart = CartItem.objects.filter(cart_id=cart)
		serialized_items = CartItemSerializer(user_cart, many=True)

		if serialized_items.data == []:
			response.data['cart'] = 'You have no item in your cart'
		else:
			sub_total = AmountCalculationHelper.get_actual_total(user_cart)
			response.data['cart'] = serialized_items.data
			response.data['total'] = sub_total
		return(response)

class CouponViewsSet(generics.ListAPIView):
	permission_classes = (AllowAny,)
	serializer_class = CouponSerializer
	my_tags = ['Checkout']

	def get(self, request):

		response = Response()
		response.data = {}
		
		active_coupons = Coupon.objects.filter(active=True)
		serialized_items = CouponSerializer(active_coupons, many=True)

		if serialized_items.data == []:
			response.data['details'] = 'There are no active coupons!'
		else:
			res = []
			for coupon in active_coupons:
				ser = CouponSerializer(coupon)
				res.append({
					ser.data['code']: ser.data['description']
					})

			response.data['available_coupons'] = res

		return(response)

class Checkout(generics.CreateAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = ApplyCouponSerializer
	my_tags = ['Checkout']


	def get_queryset(self):
		cart = Cart.objects.get(customer_id=self.request.user.id)
		return CartItem.objects.filter(cart_id=cart)


	def post(self, request):
		response = Response()
		response.data = {}

		coupon_code = request.data['coupon']

		cart = Cart.objects.get(customer_id=self.request.user.id)
		user_cart = CartItem.objects.filter(cart_id=cart)
		serialized_items = CartItemSerializer(user_cart, many=True)


		if serialized_items.data != []:
			actual_total = AmountCalculationHelper.get_actual_total(user_cart)

			response.data['cart'] = serialized_items.data
			response.data['sub_total'] = actual_total

			try:
				coupon = Coupon.objects.get(code=coupon_code)
				if coupon.is_usable() and coupon.has_been_redeemed(request.user) == False:
					discount_percent = int(coupon.value)
					discounted_total = AmountCalculationHelper.get_discount_total(
						discount_percent, actual_total)
					response.data['detail'] = "Coupon Added Successfully!"
					response.data['discounted_total'] = discounted_total

					coupon.use_coupon()
					CheckoutHelper.track_coupon_use(customer=request.user, coupon=coupon)
				
				elif coupon.has_been_redeemed(request.user) == True:
					response.data['detail'] = "Coupon Has Been Redeemed!"
					discounted_total = actual_total
					response.data['discounted_total'] = discounted_total
				else:
					response.data['detail'] = "Coupon Expired!"
					discounted_total = actual_total
					response.data['discounted_total'] = discounted_total

			except Coupon.DoesNotExist:
				response.data['detail'] = "Invalid coupon code!"
				discounted_total = actual_total
				response.data['discounted_total'] = actual_total
				coupon = None

			CheckoutHelper.perform_checkout(cart, coupon, actual_total, discounted_total)
		else:
			response.data['cart'] = "You have no item in your cart"
		return response

class MakePaymentView(generics.CreateAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = PaymentDetailSerializer
	my_tags = ['Checkout']

	def get_queryset(self):
		cart = Cart.objects.get(customer_id=self.request.user.id)
		return CartItem.objects.filter(cart_id=cart)

	def post(self, request):
		response = Response()

		details = request.data
		cart = Cart.objects.get(customer=request.user)
		cart_items = CartItem.objects.filter(cart_id=cart)		
		if not cart_items.exists():
			response.data = {'details': "Your cart is currently empty"}
		else:
			final_checkout = CheckedOutOrder.objects.get(cart_id=cart)

			final_price = final_checkout.discounted_total

			card_token = StripePaymentGateway.generate_card_token(**details,)
			payment = StripePaymentGateway.create_payment_charge(card_token, final_price)
			
			if payment == True:
				response.data = {'status':200,'message':"Payment Successful!",}
				final_checkout.success = True
				final_checkout.save()

		return response
