from django.contrib import admin
from .models import Coupon,TrackCoupon,CheckedOutOrder
# Register your models here.
admin.site.register((Coupon, TrackCoupon, CheckedOutOrder))
