from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('cart', views.AddItemToCart, 'cart')

urlpatterns = [
	path('api/v1/', include(router.urls))
]
