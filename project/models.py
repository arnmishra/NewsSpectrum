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

    def __init__(self, name, email, username, password, active=True):
        self.name = name
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)
        self.political_score = 0
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

@login.user_loader
def load_user(id):
    return User.query.get(int(id))