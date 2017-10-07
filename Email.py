"""
This module uses gmail as its emailing app
For best results, it might be necessary to log into the gmail account and allow access for less secure apps
See: https://www.google.com/settings/security/lesssecureapps
"""


import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from GMAIL_PWD import GMAIL_PWD



class Email():
	def __init__(self, msg_file):
		self.msg_file = msg_file

	def send_gmail():
		with open(self.msg_file, mode = "rb") as message:
			msg = MIMEText(message.read(), "html", "html")

	msg["Subject"] = "Hourly Weather {}".format(datetime.now().strftime("%Y-%m-%d %H:%M"))
	msg["From"] = "vickeyakinmade22@gmail.com"
	msg["To"] = 'victorakinmade23@gmail.com, vickeyakinmade22@gmail.com'
