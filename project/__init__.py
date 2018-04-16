""" App to frontend of News Spectrum project.."""

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import indicoio, os, sys
from newsapi import NewsApiClient

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'why is this necessary'
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

if not os.path.isfile('project/credentials.txt'):
	print('Please create a credentials.txt file inside the project folder')
	sys.exit(1)
with open('project/credentials.txt') as f:
	lines = f.readlines()
	if len(lines) != 4 or lines[3] is None or lines[1] is None:
		print('Please format credentials.txt as outlined in the README.md')
		sys.exit(1)
	indicoio_api_key = lines[3]
	news_api_key = lines[1]

indicoio.config.api_key = indicoio_api_key
newsapi = NewsApiClient(api_key=str(news_api_key))

from project import models

db.drop_all()
db.create_all()

from project import views