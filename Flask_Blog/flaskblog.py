from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd4346fc699bd8adfa41f47c88698c207'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


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
    # Define houw our object is printed out
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}' ) "


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Author column created using backref in User Model

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"





posts =[
    {
        'author': 'corey',
        'title': 'blog post 1',
        'content': 'first post content',
        'date_posted':'july 1,2019'

    },
    {
        'author': 'jane',
        'title': 'blog post 2',
        'content': 'second post content',
        'date_posted':'july 2,2019'


    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register(): 
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)   


@app.route("/login", methods=['GET', 'POST'])
def login():
    # Create LoginForm object from forms.py
    form = LoginForm()
    # validate entries in the form
    if form.validate_on_submit():
        # Creating dummy data to check the login functions
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)




if __name__ == '__main__':
    app.run(debug=True)    

