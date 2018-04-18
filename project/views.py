from project import app, login, db, indicoio, newsapi
from .models import User
from flask import render_template, url_for, request, redirect
from flask_login import current_user, login_user, logout_user, login_required

@app.route("/", methods=['GET'])
@login_required
def index():
    """ Renders Home page
    :return: index.html
    """
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return render_template('index.html')
    if request.method == 'GET':
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return render_template('login.html')
    login_user(user)
    return render_template('index.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    name = request.form["name"]
    email = request.form["email"]
    username = request.form["username"]
    password = request.form["password"]
    new_user = User(name, email, username, password)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return render_template("index.html")

'''
1. Call NewsAPI get_top_headlines() to get top k articles
2. Pass these articles and their links into the NewsPaperAPI to get all the text
   for each article
3. Pass this text into the indicoio API to get political sentiment for each article
4. Make list of articles that are of certain political sentiment and return to frontend
'''
def get_top_headlines():
    sources = ['breitbart-news', 'fox-news', 'reuters', 'the-economist', 'the-new-york-times', 'buzzfeed']
    top_headlines = newsapi.get_top_headlines(sources=','.join(sources), category='general', language='en')
