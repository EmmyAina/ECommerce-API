from django.urls import include, path
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('category', views.CategoryViewSet, basename='category')

urlpatterns = [
	path('api/v1/', include(router.urls), name='category'),
	path('api/v1/category/<int:id>/products/',
	     views.ProductsinCategoryView.as_view(), name='post-in-category')
]
