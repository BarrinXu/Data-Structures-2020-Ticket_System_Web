from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from config import Config

app = Flask(__name__, static_url_path='')
app.config.from_object(Config)

bootstrap = Bootstrap(app)

login = LoginManager(app)
LoginManager.init_app(login, app)
login.login_view = 'login'
login.login_message = '您必须登录才能访问这个页面'
login.login_message_category = 'info'

from app.routes import *  # 这一行必须放在最后！
