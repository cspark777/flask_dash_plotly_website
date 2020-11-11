#source/__init__.py

import os

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = '1'
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = '1'

from flask_dance.contrib.google import make_google_blueprint, google
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
import settings


#static_path = os.path.dirname('source/static/')
#print(static_path)
basedir = os.path.abspath(os.path.dirname(__file__))
static_path = basedir + "/static/"
app = Flask(__name__, static_folder=static_path)

app.config['SECRET_KEY'] = 'myscecret'


##################
####Database Setup
basedir = os.path.abspath(os.path.dirname(__file__))
TOP_LEVEL_DIR = os.path.abspath(os.curdir)


app.config['UPLOADED_IMAGES_DEST'] = TOP_LEVEL_DIR + '/source/static/posts/'
app.config['UPLOADED_IMAGES_URL'] = '/posts/'


app.config['MAIL_SERVER']=settings.MAIL_SERVER
app.config['MAIL_PORT'] = settings.MAIL_PORT
app.config['MAIL_USERNAME'] = settings.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = settings.MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

##################

####Mail Config
mail = Mail(app)



from source.core.views import core
from source.error_pages.handler import error_pages
from source.backend.views import backend

app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(backend)

from .dash.bot_chart import init_botchart
app = init_botchart(app)
