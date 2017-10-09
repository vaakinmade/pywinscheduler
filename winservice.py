"""
Install wheelfor python
Run post install script copying DLLs to /WINDOWS/system32
Run the scheduled task as a windows service
"""


from weather import Weather
from htmlhandler import HtmlHandler
from emailserver import EmailService
from collections import OrderedDict
import schedule

# Windows Service imports
import win32service         
import win32serviceutil  
import win32event