from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register('checkout', views.CheckoutCart, 'cart')

# urlpatterns = [
# 	path('api/v1/', include(router.urls))
# ]
urlpatterns = [
    path('api/v1/cart/checkout/list',
         views.CheckoutCartItems.as_view(), name='order-from-cart'),
    path('api/v1/cart/checkout',
         views.Checkout.as_view(), name='order-from-cart'),
    path('api/v1/cart/coupons',
         views.CouponViewsSet.as_view(), name='order-from-cart'),
    path('api/v1/cart/order',
         views.MakePaymentView.as_view(), name='order-from-cart'),
]
