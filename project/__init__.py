""" App to frontend of News Spectrum project.."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import indicoio
from newsapi import NewsApiClient

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with open('project/credentials.txt') as f:
	lines = f.readlines()
	indicoio_api_key = lines[3]
	news_api_key = lines[1]

indicoio.config.api_key = indicoio_api_key
newsapi = NewsApiClient(api_key=str(news_api_key))

from project import models

db.drop_all()
db.create_all()

from project import views