# Import the database object (db) from the main application module
import datetime
from app import db,app
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import deferred
from sqlalchemy import Column

class Users(db.Model):
    __tablename__ = "users"
    email = db.Column('email',db.String(50),primary_key=True)
    username = db.Column('username', db.String(50))
    fullname = db.Column('fullname' , db.String(100))
    password = db.Column('password' , db.String(250))
    bio = deferred(Column('bio', db.Text))
    country = db.Column('country', db.String(50))
    registered_on = db.Column('registered_on' , db.DateTime)
    email_confirmation_sent_on = db.Column(db.DateTime, nullable=True)
    email_confirmed = db.Column(db.Boolean, nullable=True, default=False)
    email_confirmed_on = db.Column(db.DateTime, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, email,password,username='',fullname='',bio='',country='', email_confirmation_sent_on=None):
        self.username = username
        self.set_password(password)
        self.email = email
        self.fullname = fullname
        self.bio = bio
        self.country = country
        self.registered_on = datetime.datetime.utcnow()
        self.email_confirmation_sent_on = email_confirmation_sent_on
        self.email_confirmed = False
        self.email_confirmed_on = None

    def set_password(self , password):
        self.password = generate_password_hash(password)

    def check_password(self , password):
        return check_password_hash(self.password , password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email

    def __repr__(self):
        return '<User %r>' % (self.email)


class Score (db.Model):
    __tablename__ = "Score"
    score_id = db.Column('score_id', db.String(50), primary_key = True)
    score_level = db.Column('score_level', db.Integer)
    score_percent = db.Column('score_percent', db.Integer)
    user_u_email = db.Column('User_email', db.String(50), db.ForeignKey('users.email'))
    user = db.relationship('Users', foreign_keys=user_u_email)

    def __init__(self , score_id ,score_level ,score_percent ,user_u_email,user):
        self.score_id = score_id
        self.score_level = score_level
        self.score_percent = score_percent
        self.user_u_email = user_u_email
        self.user = user

    def __repr__(self):
        return 'Score %r' % self.score_id

class WordBank (db.Model):
    __tablename__ = "Word_Bank"
    wb_collection = deferred(Column('wb_collection', db.Text))
    wb_id = db.Column('wb_id', db.Integer, primary_key = True)
    user_wb = db.Column('user_wb', db.String(50), db.ForeignKey('users.email'))
    user = db.relationship('Users', foreign_keys=user_wb)

    def __init__(self ,wb_collection ,user_wb ,user):
        self.wb_collection = wb_collection
        self.user_wb = user_wb
        self.user = user

    def __repr__(self):
        return 'WordBank %r' % self.wb_id

category = db.Table("Movie",
    db.metadata,
    db.Column("id", db.Integer, primary_key = True),
    db.Column("category_id", db.String(11), db.ForeignKey("Categories.category_id")),
    db.Column("movie_id", db.String(11), db.ForeignKey("movies.movie_id")),
    )

class Movie(db.Model):
    __tablename__ = 'movies'
    movie_id = db.Column('movie_id', db.String(11), primary_key=True)
    movie_thumbnail = db.Column('movie_thumbnail', db.String(200))
    movie_thumbnail2 = db.Column('movie_thumbnail2', db.String(200))
    movie_name = db.Column('movie_name', db.String(200))
    movie_description = deferred(Column('movie_description', db.Text))
    category = db.relationship("Categories",
                               secondary=category,
                               backref=db.backref("movies", lazy="dynamic"),
                               )


    def __init__(self, movie_id, movie_thumbnail,movie_thumbnail2,movie_name,movie_description):
        self.movie_id = movie_id
        self.movie_thumbnail = movie_thumbnail
        self.movie_thumbnail2 = movie_thumbnail2
        self.movie_name = movie_name
        self.movie_description = movie_description

    def __repr__(self):
        return self.movie_name

class Categories(db.Model):
    __tablename__ = "Categories"
    category_id = db.Column('category_id', db.String(11), primary_key=True)
    category_name = db.Column('category_name', db.String(50))
    category_url = db.Column('category_url', db.String(100))

    def __init__(self,category_id,category_name,category_url):
        self.category_id = category_id
        self.category_name = category_name
        self.category_url = category_url

    def __repr__(self):
        return self.category_name

class InviteCode(db.Model):
    __tablename__ = "InviteCode"
    invite_code_id = db.Column('invite_code_id', db.Integer, primary_key=True)
    invite_code = db.Column('invite_code', db.String(33))

    def __init__(self, invite_code):
        self.invite_code = invite_code

    def __repr__(self):
        return self.invite_code_id