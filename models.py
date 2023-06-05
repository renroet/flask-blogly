"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

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
    

  