from project import app, login, db, indicoio
from .scripts.get_headlines import get_top_headlines, calculate_political_score
from .models import User, Articles
from flask import render_template, url_for, request, redirect, make_response, Response
from flask_login import current_user, login_user, logout_user, login_required
from random import shuffle
import json
from newspaper import Article


@app.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        if current_user.political_score == 0:
            return render_template('index.html')
        else:
            get_top_headlines()
            articles = []
            for score in current_user.target_scores:
                articles += Articles.query.filter(Articles.political_leaning == score).all()
                shuffle(articles)
            return render_template('profile.html', user=current_user.name, articles=articles)
    elif request.method == 'GET':
        return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return render_template('login.html')
    login_user(user, remember=True)
    resp = make_response(redirect('/'))
    resp.set_cookie('username', username)
    return resp 

@app.route('/logout')
def logout():
    logout_user()
    res = make_response(redirect('/'))
    if request.cookies.get('username'):
        res.set_cookie('username', '', expires=0)
    return res

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
    elif request.method == 'GET':
        return redirect('/')

@app.route('/load_news_page/<article_id>', methods=['POST'])
def load_new_page(article_id=-1):
    if article_id == -1:
        return redirect("/")
    return render_template("news_page.html", article=Articles.query.get(article_id), user=current_user.name)

@app.route('/article_review', methods=['POST'])
def article_review():
    score = request.form["score"]
    if score == current_user.political_score:
        return redirect("/")
    if request.form["review"] == "disliked":
        current_user.change_score += 1
    else:
        current_user.change_score -= 1
    if current_user.change_score == 0:
        current_user.set_score(current_user.target_scores[1])
    db.session.commit()
    print (current_user.change_score)
    return redirect("/")

@app.route('/chrome_extension', methods=['POST'])
def chrome_extension():
    if request.method == 'POST':
        data = json.loads(request.data)
        article = Article(data['url'],"en")
        article.download()
        article.parse()
        text = article.text
        political_leaning = indicoio.political(text)
        score = calculate_political_score(political_leaning["Liberal"], political_leaning["Conservative"])
        print("URL: ", data['url'])
        print(political_leaning)
        print("Political score: ", score)
    return Response(status=200)

