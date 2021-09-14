from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
base = 'api/v1/account/'

router = DefaultRouter()
# router.register('profile', views.UpdateBioViewSet, 'bio')
router.register('user', views.User, 'user-info')



urlpatterns = [
	path('api/v1/', include(router.urls)),
	path(base+'signup', views.RegisterView.as_view(), name='register'),
	path(base+'email-verify', views.VerifyEmail.as_view(), name='email-verify'),


	# path(base+'forgot-password', views.RequestPasswordResetView.as_view(),
	#      name='forgot-password'),
	# path(base+'reset-password', views.ResetPasswordView.as_view(), name='reset-password'),
]
