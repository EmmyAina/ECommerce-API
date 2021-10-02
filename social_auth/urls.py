from django.urls.resolvers import URLPattern
from .views import GoogleSocialAuthView
from django.urls import path

urlpatterns = [
	path("api/v1/social_auth/google/", GoogleSocialAuthView.as_view())
]
