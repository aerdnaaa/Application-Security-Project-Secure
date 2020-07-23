import os, datetime

DEBUG = True
SECRET_KEY = 'WeakSecret'
SESSION_COOKIE_HTTPONLY = True
JWT_SECRET_KEY = 'super-secret'
# MAIL_SERVER ='smtp.mailtrap.io'
# MAIL_PORT = 2525
# MAIL_USERNAME = '30f5c0135695dc'
# MAIL_PASSWORD = 'c0a826e1a62988'
# MAIL_USE_TLS = True
# MAIL_USE_SSL = False

# Send email through Gmail
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'ballsnpaddles@gmail.com'
MAIL_PASSWORD = 'ionevvqefbbwmcip'