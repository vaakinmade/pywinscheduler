from footyapi import FootballDataAPI
from htmlhandler import HtmlHandler
from emailserver import EmailService

from collections import OrderedList
from time import sleep
from pprint import pprint
import schedule

class Schedule():
	@classmethod
	def job(cls):
		pprint(schedule.jobs)
		list_dict = FootballDataAPI().retrieve_matchday_fixtures()  
		footy_dict_ordered = OrderedList(sorted(list_dict))

		email_file = "Email_File.html"
		HtmlHandler.create_html_file(footy_dict_ordered, "Email_File.html")
		EmailService(email_file).send_email()


schedule.every().hour.do(job)
schedule.every(1).minutes.do(Schedule.job)


while True:
	schedule.run_pending()
	sleep(1)