"""
This module uses gmail as its emailing app
For best results, it might be necessary to log into the gmail account and allow access for less secure apps
See: https://www.google.com/settings/security/lesssecureapps
"""


import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from GMAIL_PWD import GMAIL_PWD

