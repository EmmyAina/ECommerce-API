from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('coupons', views.CouponViewSet, 'coupons')
router.register('checkout/items',views.CheckedOutItemsViewset, 'checked-out-items')
# router.register('cart/checkout/', views.PerformCheckout, 'checkout-cart')


# urlpatterns = [
#     path('api/v1/cart/checkout/list',
#          views.CheckoutCartItems.as_view(), name='order-from-cart'),
#     path('api/v1/cart/checkout',
#          views.Checkout.as_view(), name='order-from-cart'),

# ]
urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/cart/order',
         views.MakePaymentView.as_view(), name='order-from-cart'),
    path('api/v1/cart/checkout',
        views.Checkout.as_view(), name='order-from-cart'),
]
