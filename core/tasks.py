from __future__ import absolute_import
from django.core.mail import send_mail
# from celery import shared_task
from decouple import config
from celery import Celery
import time

app = Celery('tasks', backend="redis", broker=config("REDIS_URL"))


class Tasks:
	@staticmethod
	@app.task
	def send_verification_mail(data):
		mail = send_mail(
			data['subject'],
			data['body'],
			data['sender'],
			data['recepient']
		)
		return "Mail Sent Successfully"
