from rest_framework import status
from Test.test_setup import TestSetup,set_to_admin,verify
from Auth.models import TokenModel
from faker import Faker
# Create your tests here.

class Auth_TestCase(TestSetup):

	def test_can_register(self):
		response = self.client.post(self.register_url, self.register_data)
		success = response.data['success']

		self.assertTrue(success)
		self.assertEqual(response.data['message'],"Account created successfully. Check your mail to verify your account")
		return self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_user_can_login(self):
		self.client.post(self.register_url, self.register_data)
		verify(self.register_data['email'])
		set_to_admin(self.register_data['email'])
		login_response = self.client.post(self.login_url, self.login_data)
		token = login_response.data['access']

		success = login_response.data['success']

		self.assertTrue(success)
		self.assertIsNotNone(token)

		return self.assertEqual(login_response.status_code, status.HTTP_200_OK)

	def test_cannot_register(self):
		response = self.client.post(self.register_url)
		return self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_user_cannot_login(self):
		self.client.post(self.login_url, self.register_data)
		bad_login_data = {
			"email": Faker().email(), "password": Faker().password()}
		login_response = self.client.post(self.login_url, bad_login_data)

		success = login_response.data['success']
		self.assertFalse(success)
		return self.assertEqual(login_response.status_code, status.HTTP_403_FORBIDDEN)

	def test_token_creation(self):
		self.client.post(self.register_url, self.register_data)
		verify(self.register_data['email'])
		set_to_admin(self.register_data['email'])
		login_response = self.client.post(self.login_url, self.login_data)
		token = login_response.data['access']
		self.assertIsNotNone(token)
		return self.assertEqual(len(token), 255)
