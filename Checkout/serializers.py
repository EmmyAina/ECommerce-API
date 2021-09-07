from rest_framework import serializers
from Cart.models import Cart

class OrderItemSerializer(serializers.ModelSerializer):
    coupon = serializers.CharField(max_length=7)

    class Meta:
        model = Cart
        fields = ('coupon',)

    def validate(self, data):
        coupoun_value = data.get('coupoun_code')

        if not coupoun_value:
            pass

        data['coupon_value'] = coupoun_value

        return data
