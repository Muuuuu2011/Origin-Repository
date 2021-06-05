from flask import *
from flask_mail import Mail
import os
from dotenv import load_dotenv


load_dotenv()

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['SECRET_KEY'] = os.getenv('conf_secret_key')
app.config['DEBUG']=True
app.config['TESTING']=False
app.config['MAIL_SERVER']=os.getenv('conf_mail_server')
app.config['MAIL_PORT']=os.getenv('conf_mail_port')
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USE_SSL']=False
app.config['MAIL_USERNAME']=os.getenv('conf_mail_user')
app.config['MAIL_PASSWORD']=os.getenv('conf_mail_password')
app.config['MAIL_DEFAULT_SENDER']=os.getenv('conf_mail_user')
app.config['MAIL_MAX_EMAILS']=None
app.config['MAIL_ASCII_ATTACHMENTS']=False
#  記得先設置參數再做實作mail
mail = Mail(app)



