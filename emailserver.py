"""
This module uses gmail as its emailing server
For best results, it might be necessary to log into the gmail account and allow access for less secure apps
See: https://www.google.com/settings/security/lesssecureapps
"""


import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from gmail_key import GMAIL_PWD



class EmailService():
	def __init__(self, msg_file):
		self.msg_file = msg_file

	def read_message(self):
		with open(self.msg_file, mode = "rb") as message:
			msg = MIMEText(message.read(), "html", "html")

		msg["Subject"] = "Hourly Weather {}".format(datetime.now().strftime("%Y-%m-%d %H:%M"))
		msg["From"] = "vickeyakinmade22@gmail.com"
		msg["To"] = 'victorakinmade23@gmail.com, vickeyakinmade22@gmail.com'
		return msg

	def send_message(self):
		server = smtplib.SMTP('smtp.gmail.com', port=587)
		server.ehlo()       # Extended Hello
		server.starttls()   # Put the SMTP connection in TLS (Transport Layer Security) mode.  
		server.ehlo()       # All SMTP commands that follow will be encrypted.
		server.login('vickeyakinmade22@gmail.com', GMAIL_PWD)
		server.send_message(self.read_message())
		server.close()


if __name__ == '__main__':
    from weather import Weather
    from htmlhandler import HtmlHandler #import create_html_file 
    weather_dict, icon = Weather('KLAX').get_data_iconurl()
    email_file = "Test_Email_File.html"
    HtmlHandler().create_html_file(weather_dict, icon, email_file)
    EmailService(email_file).send_message()