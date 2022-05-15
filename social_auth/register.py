from django.contrib.auth import authenticate
from decouple import config
from Account.models import User
from random import randint
from rest_framework.exceptions import AuthenticationFailed
from Auth.authentication import Authentication

def generate_user_name(name):
	username = "".join(name.split(' ')).lower()
	if User.objects.filter(username=username).exists():
		random_username = username + str(randint(0,1000))
		return generate_user_name(random_username)
	else:
		return username

def register_social_user(provider, email, user_id, name):
	filtered_user_by_email = User.objects.filter(email=email)

	if filtered_user_by_email.exists():
		# If an already registered user tries to register again, perform direct login
		if provider == filtered_user_by_email[0].auth_provider:

			registered_user = authenticate(email=email, password= config("ECOMM_SECRETKEY"))
			token = Authentication.create_token_for_user(registered_user)
			login_data = {
				"username":registered_user.username,
				"email": registered_user.email,
				"access": token['access'],
				"refresh": token['refresh']
			}
			return login_data
		else:
			raise AuthenticationFailed(
				detail=f"Please login with your {filtered_user_by_email[0].auth_provider} account"
			)
	else:
		user = {
			"email": email,
			"username": generate_user_name(name),
			"password": config('ECOMM_SECRETKEY'),
			"verified":True,
			"auth_provider": provider,
		}

		user = User.objects.create_user(**user)

		user.save()

		new_user = authenticate(email=user.email , password=config("ECOMM_SECRETKEY"))
		token = Authentication.create_token_for_user(new_user)
		return {
			"email":new_user.email,
			"username":new_user.username,
			"access": token['access'],
			"refresh":token['refresh'],
		}
