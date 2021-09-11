from django.http import request
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet, ViewSet
from Cart.models import Cart
from .serializers import ApplyCouponSerializer, PaymentDetailSerializer, CouponSerializer, CheckedOutSerializer
from rest_framework.generics import GenericAPIView
from .stripe_api import StripePaymentGateway
from rest_framework.exceptions import AuthenticationFailed
from Cart.models import Cart, CartItem
from Cart.serializers import CartItemSerializer
from Checkout.models import Coupon, CheckedOutOrder
from .helper import AmountCalculationHelper, CheckoutHelper

##---------------ViewSet to retrieve active coupons and description ---------------
class CouponViewSet(ReadOnlyModelViewSet):
	my_tags = ['Checkout']
	queryset = Coupon.objects.all()
	serializer_class = CouponSerializer

	def get_queryset(self):
		return self.queryset.filter(active=True)

#---------------Viewset to retrieve checked out cart ---------------
class CheckedOutItemsViewset(ReadOnlyModelViewSet):
	my_tags = ["Checkout"]
	queryset = CheckedOutOrder.objects.all()
	serializer_class = CheckedOutSerializer

	def get_queryset(self):
		return self.queryset.get(cart_id =self.request.user.id)
	
	def list(self, request, *args, **kwargs):
		instance = self.get_queryset()
		serializer = self.get_serializer(instance)
		response = Response()
		response.data = serializer.data
		items = CartItem.objects.filter(cart_id=self.request.user.id)
		ser_items = CartItemSerializer(items,many=True)
		response.data['products'] = ser_items.data

		return response

#---------------APIView to apply coupon and checkout a user cart ---------------
class Checkout(GenericAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = ApplyCouponSerializer
	my_tags = ['Checkout']
	queryset = Cart.objects.all()


	def get_queryset(self):
		return self.queryset.get(id=self.request.user)

	def post(self, request):
		response = Response()
		response.data = {}

		coupon_code = request.data['coupon']

		user_cart_items = CartItem.objects.filter(cart_id=self.get_queryset())
		serialized_items = CartItemSerializer(user_cart_items, many=True)

		if serialized_items.data != []:
			actual_total = AmountCalculationHelper.get_actual_total(user_cart_items)

			response.data = {'cart' : serialized_items.data,'sub_total' : actual_total}

			try:
				coupon = Coupon.objects.get(code=coupon_code)
				if coupon.is_usable() and coupon.has_been_redeemed(request.user) == False:
					discounted_total = AmountCalculationHelper.get_discount_total(int(coupon.value), actual_total)
					response.data['detail'], response.data['discounted_total'] = "Coupon Added Successfully!",discounted_total
					coupon.use_coupon()
					CheckoutHelper.track_coupon_use(customer=request.user, coupon=coupon)
				elif coupon.has_been_redeemed(request.user) == True:
					discounted_total = actual_total
					response.data['detail'], response.data['discounted_total'] = "Coupon Has Been Redeemed!", actual_total
				else:
					discounted_total = actual_total
					response.data['detail'], response.data['discounted_total'] = "Coupon Expired!", actual_total
			except Coupon.DoesNotExist:
				discounted_total = actual_total
				response.data['detail'], response.data['discounted_total'] = "Invalid coupon code!", actual_total
				coupon = None
			CheckoutHelper.perform_checkout(self.get_queryset(), coupon, actual_total, discounted_total)
		else:
			response.data['cart'] = "You have no item in your cart"
		return response

#---------------APIView to make payment through stripe ---------------
class MakePaymentView(GenericAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = PaymentDetailSerializer
	my_tags = ['Checkout']
	queryset = Cart.objects.all()

	def get_queryset(self):
		return self.queryset.get(id=self.request.user)

	def post(self, request):
		response = Response()
		details = request.data

		cart_items = CartItem.objects.filter(cart_id=self.get_queryset())		
		if not cart_items.exists():
			response.data = {'details': "Your cart is currently empty"}
		else:
			final_checkout = CheckedOutOrder.objects.get(cart_id=self.get_queryset())
			final_price = int(final_checkout.discounted_total)

			card_token = StripePaymentGateway.generate_card_token.delay(**details,).get()
			payment = StripePaymentGateway.create_payment_charge.delay(card_token, final_price).get()
			
			if payment == True:
				response.data = {'status':200,'message':"Payment Successful!",}
				final_checkout.success = True
				final_checkout.save()

		return response
