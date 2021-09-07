from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('product', views.ProductViewSet, 'product')

urlpatterns = [
	path('api/v1/', include(router.urls))
]
