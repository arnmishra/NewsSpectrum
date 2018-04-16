from project import app, login, db, indicoio, newsapi
from models import User
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
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return render_template('login.html')
    login_user(user, remember=form.remember_me.data)
    return render_template('index.html')

@app.route('/logout')
def logout():
    logout_user()
    return render_template('index.html')

