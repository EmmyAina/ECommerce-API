from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
import pdb
from Test.test_setup import TestSetup, set_to_admin,verify


class Categories_TestCase(TestSetup):

	def test_admin_can_create_category(self):
		self.client.post(self.register_url, self.register_data)
		set_to_admin(self.register_data['email'])
		verify(self.register_data['email'])
		login_response = self.client.post(self.login_url, self.login_data)

		token = login_response.data['access']
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

		response = self.client.post(self.category_url, self.category_data)

		category = response.data['category_name']

		self.assertIsNotNone(category)
		self.assertEqual(category, self.category_data['category_name'])
		return self.assertEqual(response.status_code, 201)

	def test_user_cannot_create_category(self):
		self.client.post(self.register_url, self.register_data)
		verify(self.register_data['email'])
		login_response = self.client.post(self.login_url, self.login_data)

		token = login_response.data['access']
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

		response = self.client.post(self.category_url, self.category_data)
		return self.assertEqual(response.status_code, 403)

	def test_get_categories_without_login(self):
		response = self.client.get(self.category_url)
		print(response.data)
		return self.assertEqual(response.status_code, 200)
