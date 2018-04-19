from project import app, login, db
from .scripts.get_headlines import get_top_headlines
from .models import User
from flask import render_template, url_for, request, redirect
from flask_login import current_user, login_user, logout_user, login_required

ARTICLES = []

@app.route('/', methods=['GET'])
def index():
    global ARTICLES
    if current_user.is_authenticated:
        if current_user.political_score == 0:
            ARTICLES = get_top_headlines(current_user)
            return render_template('index.html', user=current_user.name, articles=ARTICLES)
        else:
            ARTICLES = get_top_headlines(current_user)
            return render_template('profile.html', user=current_user.name, articles=ARTICLES)
    elif request.method == 'GET':
        return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return render_template('login.html')
    login_user(user)
    if user.political_score != 0:
        return redirect('/')
    return redirect('/')

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

@app.route('/political-typology', methods=['POST'])
def political_typology():
    if current_user.is_authenticated:
        if request.method == 'POST':
            political_typology = request.form["political_typology"]

            mapPoliticalTypologyToScore = {
                "Solid Liberals": 1,
                "Opportunity Democrats": 2,
                "Disaffected Democrats": 3,
                "Devout and Diverse": 4,
                "New Era Enterprisers": 5,
                "Market Skeptic Republicans": 6,
                "Country First Conservaties": 7,
                "Core Conservatives": 8,
                "Bystanders": 9
            }

            try:
                political_score = mapPoliticalTypologyToScore[political_typology]
                current_user.set_score(political_score)
                db.session.commit()
            except:
                print("Error converting political typology to political score: " + political_typology)

            return redirect('/')
            # return render_template('profile.html', user=current_user.name, articles=articles)
    elif request.method == 'GET':
        return redirect('/')

@app.route('/load_news_page', methods=['POST'])
def load_new_page():
    article_name = request.form["article_name"]
    return render_template("news_page.html", article=ARTICLES[article_name], user=current_user.name)

@app.route('/article_review', methods=['POST'])
def article_review():
    score = request.form["score"]
    if request.form["review"] == "disliked":
        current_user.change_score += 1
    else:
        current_user.change_score -= 1
    if current_user.change_score == 0:
        current_user.set_score(current_user.target_score[1])
