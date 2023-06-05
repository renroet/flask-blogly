"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from sqlalchemy.sql import text

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
# db.create_all()

@app.route('/')
def redirect_users():
    return redirect('/users')

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def add_user_form():
    return render_template('new_user.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    image_url = request.form["image_url"]

    if image_url == "":
        image_url = None

    new_user = User(first_name=first_name, last_name=last_name, email=email, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()
    # id = new_user.id

    return redirect(f'/users/{new_user.id}')

@app.route('/users/<int:user_id>')
def details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    image_url = request.form["image_url"]

    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.image_url = image_url

    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def user_delete(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


# flash messaging
# docstrings