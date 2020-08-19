from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
import os, sqlite3
import logging
import sentry_sdk
from flask_restful import Api
from flask_login import LoginManager
from flaskr.models.User import User
from flask_wtf.csrf import CSRFProtect,CSRFError

# sentry sdk for logging
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.flask import FlaskIntegration

# All of this is already happening by default!
sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)
sentry_sdk.init(
    dsn="https://6adb767a90f14dee90f656e1e355f0b1@o412137.ingest.sentry.io/5288433",
    integrations=[FlaskIntegration()]
)

app = Flask(__name__)
api_app = Api(app)
csrf = CSRFProtect(app)
CORS(app, supports_credentials=True)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='ballsnpaddles@gmail.com',
    MAIL_PASSWORD='ionevvqefbbwmcip'
)
mail = Mail(app)

login_manager = LoginManager(app)
app.config.from_object('config')

file_directory = os.path.dirname(os.path.dirname(__file__))

from flaskr.api.products import Products
from flaskr.api.vouchers import Vouchers
from flaskr.api.user_voucher import UserVoucher
from flaskr.api.login import Login

api_app.add_resource(Login, '/api/login')
api_app.add_resource(Products, '/api/products')
api_app.add_resource(Vouchers, '/api/vouchers')
api_app.add_resource(UserVoucher, '/api/userVoucher/<user_id>')

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
    c.execute("SELECT * FROM users WHERE user_id=? ", (user_id,))
    conn.commit()
    user = c.fetchone()
    conn.close()
    userObj = User(user[0], user[1], user[2], user[3], user[4])
    return userObj


@app.after_request
def apply_caching(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers['X-Content-Type-Options'] = "nosniff"
    return response