from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
import os, sqlite3
import logging
import sentry_sdk
from flask_login import LoginManager
from flaskr.models.User import User

# # sentry sdk for logging
# from sentry_sdk.integrations.logging import LoggingIntegration
# from sentry_sdk.integrations.flask import FlaskIntegration
#
# # All of this is already happening by default!
# sentry_logging = LoggingIntegration(
#     level=logging.INFO,  # Capture info and above as breadcrumbs
#     event_level=logging.ERROR  # Send errors as events
# )
# sentry_sdk.init(
#     dsn="https://6adb767a90f14dee90f656e1e355f0b1@o412137.ingest.sentry.io/5288433",
#     integrations=[FlaskIntegration()]
# )

app = Flask(__name__)
api_app = Api(app)
jwt = JWTManager(app)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'ballsnpaddles@gmail.com',
    MAIL_PASSWORD = 'ionevvqefbbwmcip'
)
mail = Mail(app)
CORS(app)
login_manager = LoginManager(app)
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LfmcrMZAAAAAJcTRMYVFIii7-reRZ4a_o5V1m37'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LfmcrMZAAAAAL_V-ZYV0CDySlbKLzhgi5DqYd8Q'
app.config.from_object('config')

file_directory = os.path.dirname(os.path.dirname(__file__))

from flaskr.api.products import Products
from flaskr.api.vouchers import Vouchers
from flaskr.api.user_voucher import UserVoucher

api_app.add_resource(Products, '/api/products')
api_app.add_resource(Vouchers, '/api/vouchers')
api_app.add_resource(UserVoucher, '/api/userVoucher/<username>')

from flaskr.views.admin import admin_blueprint
from flaskr.views.main import main_blueprint
from flaskr.views.shopping import shopping_blueprint
from flaskr.views.user import user_blueprint

app.register_blueprint(admin_blueprint)
app.register_blueprint(main_blueprint)
app.register_blueprint(shopping_blueprint)
app.register_blueprint(user_blueprint)


@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0


@app.route('/issues')
def sentry_issues():
    return ("https://sentry.io/api/0/project/Indirect/Indirect/issues/")

# Flask Login User Loader
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM users WHERE rowid={} ".format(user_id))
    conn.commit()
    user = c.fetchone()
    conn.close()
    userObj = User(user[0], user[1], user[2], user[3], user[4])
    return userObj
