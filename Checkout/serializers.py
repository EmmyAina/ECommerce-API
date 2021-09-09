from Checkout.models import Coupon
from rest_framework import serializers
from Cart.models import CartItem


class ApplyCouponSerializer(serializers.ModelSerializer):
    coupon = serializers.CharField(max_length=7)

    class Meta:
        model = CartItem
        fields = ('coupon',)

    def validate(self, data):
        coupoun_value = data.get('coupoun_code')

        if not coupoun_value:
            pass

        data['coupon_value'] = coupoun_value

        return data

class CouponSerializer(serializers.ModelSerializer):
	class Meta:
		model = Coupon
		fields = '__all__'

class PaymentDetailSerializer(serializers.Serializer):
	cardnumber = serializers.CharField(max_length=16)
	cvv = serializers.CharField(max_length=3)
	exp_month = serializers.CharField(max_length=2)
	exp_year = serializers.CharField(max_length=4)
	address_line1 = serializers.CharField(max_length=255)
	address_state = serializers.CharField(max_length=255)
	address_country = serializers.CharField(max_length=255)
