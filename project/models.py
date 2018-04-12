from project import db

class User(db.Model):
    """ User Model with all data about a specific user. """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.Integer)
    username = db.Column(db.Integer)
    password = db.Column(db.String)
    political_score = db.Column(db.Integer)

    def __init__(self, name, email, username, password, political_score):
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.political_score = political_score

    def __repr__(self):
        return "<Room(name='%s', email='%d', username='%d', score='%d')>" % (self.name, self.email, self.username, self.political_score)
