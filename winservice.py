"""
Install wheel for python
Run post install script copying DLLs to /WINDOWS/system32
Run the scheduled task as a windows service
"""


from footyapi import FootballDataAPI
from htmlhandler import HtmlHandler
from emailserver import EmailService
import schedule

''' 
Windows Service imports for pywin32
Go to gohlke libaries, download the pyWin32 wheel for python version and bit version.
Activate virtualenv
run pip install file.whl
'''
import win32service         
import win32serviceutil  
import win32event


class FootyAlertTaskSvc(win32serviceutil.ServiceFramework):  
	_svc_name_ = "FootyAlertTaskSvc"    
	_svc_display_name_ = "Python Scheduling Service for football fixture inboxer"   
	_svc_description_ = "This Python service schedules tasks"  
      
	def __init__(self, args):  
		win32serviceutil.ServiceFramework.__init__(self, args)  
		self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)  
        
	def SvcDoRun(self):  
		def job():
			obj = FootballDataAPI()
			HtmlHandler().create_html_file(
				obj.retrieve_matchday_fixtures(445),
				obj.single_team_fixtures(66),
				obj.latest_competition_results(445)
			)
			email_file = "Email_File.html"
			EmailService(email_file).send_email()
        
		#schedule.every().hour.do(job)
		schedule.every(1).minutes.do(job)   # for dev use 1 minute
        
		rc = None
		while rc != win32event.WAIT_OBJECT_0:
			schedule.run_pending()
			rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)  
            
	def SvcStop(self):  
		self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)  
		win32event.SetEvent(self.hWaitStop)  
          
if __name__ == '__main__':  
    win32serviceutil.HandleCommandLine(FootyAlertTaskSvc)