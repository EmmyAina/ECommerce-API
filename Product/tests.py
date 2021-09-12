from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
import pdb
from Account.models import User
from Test.test_setup import TestSetup, set_to_admin,verify


class Product_TestCase(TestSetup):

	def test_admin_can_create_product(self):
		self.client.post(self.register_url, self.register_data)
		verify(self.register_data['email'])
		set_to_admin(self.register_data['email'])
		login_response = self.client.post(self.login_url, self.login_data)
		token = login_response.data['access']
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

		category_resp = self.client.post(self.category_url, self.category_data)
		self.product_data['category'] = category_resp.data['id']
		response = self.client.post(self.product_url, self.product_data)

		product_price = response.data['product_price_ngn']
		self.assertIsNotNone(product_price)
		self.assertEqual(product_price, self.product_data['product_price_ngn'])
		return self.assertEqual(response.status_code, 201)

	def test_user_cannot_create_product(self):
		self.client.post(self.register_url, self.register_data)
		verify(self.register_data['email'])
		login_response = self.client.post(self.login_url, self.login_data)

		token = login_response.data['access']
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

		cat_response = self.client.post(self.category_url, self.category_data)

		self.assertEqual(cat_response.status_code, 403)
		response = self.client.post(self.product_url, self.product_data)
		return self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_get_products_without_login(self):
		response = self.client.get(self.product_url)
		return self.assertEqual(response.status_code, 200)
