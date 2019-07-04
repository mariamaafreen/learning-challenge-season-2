from datetime import datetime
from flaskblog import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    
    # Unlike above ones, 'posts' is not an attribute but a relationship - cool feature of SQLAlchemy
    # backref : Similar to adding another column to Post model
    # lazy : True - Loads data from databse; False - Doesn' load the data
    posts = db.relationship('Post', backref='author', lazy=True)

    # Magic Method
    # Define how our object is printed out
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}') "


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False) 
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Author column created using backref in User Model

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


 