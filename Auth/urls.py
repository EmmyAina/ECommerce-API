from django.urls import path, include
from . import views

base = 'api/v1/account/'
urlpatterns = [
	path(base+'login', views.LoginView.as_view(), name='login'),
	path(base+'refresh', views.RefreshTokenView.as_view(), name='refresh'),
]
