"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy.orm import backref


db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    
    email = db.Column(db.Text, 
                        nullable=False,
                        unique=True)

    first_name = db.Column(db.Text,
                            nullable=False)

    last_name = db.Column(db.Text,
                            nullable=False)
    
    image_url = db.Column(db.Text,
                            nullable=False,
                            default="https://t3.ftcdn.net/jpg/00/64/67/80/360_F_64678017_zUpiZFjj04cnLri7oADnyMH0XBYyQghG.jpg")
    

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
                
    title = db.Column(db.String(50),
                        nullable=False)

    content = db.Column(db.Text,
                        nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    created_by = db.Column(db.Integer,
                            db.ForeignKey('users.id'))
    
    users_for_post = db.relationship('User', backref=backref('posts_for_users', cascade='all,delete-orphan'))

