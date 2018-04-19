import datetime
from project import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    """ User Model with all data about a specific user. """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.Integer)
    username = db.Column(db.Integer)
    password = db.Column(db.String)
    political_score = db.Column(db.Integer) #1-9 scoring, 0 means not set
    target_scores = db.Column(db.PickleType)
    change_score = db.Column(db.Integer) #net 10 likes on articles of a different score means changing your score

    def __init__(self, name, email, username, password, active=True):
        self.name = name
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)
        self.political_score = 0
        self.target_scores = [0]
        self.active = active

    def __repr__(self):
        return "<User(name='%s', email='%s', username='%s', score='%d')>" % (self.name, self.email, self.username, self.political_score)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_active(self):
        return self.active

    def get_id(self):
        return self.id

    def set_score(self, score):
        self.political_score = score
        if score > 5:
            self.target_scores = [score, score - 1]
        elif score < 5:
            self.target_scores = [score, score + 1]
        else:
            self.target_scores = [4,5,6]
        self.change_score = 10

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Articles(db.Model):
    """ Articles Model with all data about the articles for the past day. """
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime)
    article_name = db.Column(db.String)
    source = db.Column(db.String)
    description = db.Column(db.String)
    url = db.Column(db.String)
    text = db.Column(db.String)
    political_leaning = db.Column(db.Integer) #1-9 scoring

    def __init__(self, article_name, source, description, url, text, political_leaning):
        self.creation_date = datetime.datetime.now()
        self.article_name = article_name
        self.source = source
        self.description = description
        self.url = url
        self.text = text
        self.political_leaning = political_leaning

    def __repr__(self):
        return "<Articles(article_name='%s', url='%s', political_leaning='%i')>" % (self.article_name, self.url, self.political_leaning)
