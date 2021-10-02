from google.oauth2 import id_token
from google.auth.transport import requests

class Google:
	"""
	Class for validating authentication token and returning the user information
	"""
	@staticmethod 
	def validate(token):
		"""
		Validate and fetch user info from Oauth2 api
		"""

		id_info = id_token.verify_oauth2_token(token, requests.Request())

		try:
			if 'accounts.google.com' in id_info['iss']:
				return id_info
		except:
			return 'Invalid or expired token from helper'
