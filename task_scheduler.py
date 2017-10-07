from weather import Weather
from htmlhandler import HtmlHandler
from emailserver import EmailService

from collections import OrderedDict
from time import sleep
from pprint import pprint
import schedule

class Schedule():
	@classmethod
	def job(cls):
	    pprint(schedule.jobs)
	    weather_dict, icon = Weather('KLAX').get_data_iconurl()  
	    weather_dict_ordered = OrderedDict(sorted(weather_dict.items())) 
	    
	    email_file = "Email_File.html"
	    HtmlHandler.create_html_file(weather_dict_ordered, icon, email_file)
	    EmailService(email_file).send_email()


# schedule.every().hour.do(job)
schedule.every(1).minutes.do(Schedule.job)

while True:
    schedule.run_pending()
    sleep(1)