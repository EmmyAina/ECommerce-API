from rest_framework.test import APITestCase
from Account.models import User
from faker import Faker
from django.urls import reverse


def set_to_admin(email):
	user = User.objects.get(email=email)
	user.is_superuser = True
	user.is_staff = True
	user.verified = True

	user.save()
	return user


class TestSetup(APITestCase):
	def setUp(self):
		fake_detail = Faker()
		email = fake_detail.email()
		username = fake_detail.name()
		password = fake_detail.password()
		text = fake_detail.text(max_nb_chars=100)

		self.register_url = reverse('register')
		self.register_data = {"email": email,"username": username,"gender": "Female","password": password}

		self.login_url = reverse('login')
		self.login_data = {"email": email,"password": password}

		# self.category_url = reverse('category')
		# self.category_data = {"category_name": "Sport"}

		# self.product_url = reverse('product')
		# self.product_data = {"product_name": fake_detail.text(),"product_price_ngn": fake_detail.text(),
		# "product_description": fake_detail.text(),"available_inventory": int(fake_detail.numerify()),
		# "product_image": '/ home/emmanuel/Emmanuel/Serious Projects/Construction-Store/profile_pics/user-avatar.png',
		# "category": 1}

		return super().setUp()

	def tearDown(self):
		return super().tearDown()
