import os, datetime

DEBUG = True
SECRET_KEY = 'WeakSecret'
SESSION_COOKIE_HTTPONLY = False
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=365)
JWT_SECRET_KEY = 'super-secret'
MAIL_SERVER ='smtp.mailtrap.io'
MAIL_PORT = 2525
MAIL_USERNAME = '30f5c0135695dc'
MAIL_PASSWORD = 'c0a826e1a62988'
MAIL_USE_TLS = True
MAIL_USE_SSL = False
# this is gae