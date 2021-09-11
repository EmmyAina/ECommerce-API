from django.core.mail import send_mail
# from celery import shared_task


class Utils:
	@staticmethod
	def send_verification_mail(data):
		mail = send_mail(
			data['subject'],
			data['body'],
			data['sender'],
			data['recepient']
		)
		print("Mail Sent Successfully")
		return "Mail Sent Successfully"
