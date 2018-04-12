from project import app, db, indicoio, newsapi
from models import User
from flask import render_template, url_for, request

@app.route("/", methods=['GET'])
def index():
    """ Renders Home page
    :return: index.html
    """
    return render_template("index.html")
