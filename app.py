"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
from sqlalchemy.sql import text
from sqlalchemy import exc

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.debug = True

app.config['SECRET_KEY'] = 'not-so-secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

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
    try:
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
        flash(f'{new_user.first_name} {new_user.last_name} successfully added', 'success')
        return redirect(f'/users/{new_user.id}')
    except exc.IntegrityError:
        
        flash('email address already in use', 'error')
        return redirect('/users/new')




@app.route('/users/<int:user_id>')
def details(user_id):
    user = User.query.get_or_404(user_id)
    posts = user.posts_for_users
    return render_template('user_details.html', user=user, posts=posts)

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
    username = f'{user.first_name} {user.last_name}' 
    db.session.delete(user)
    db.session.commit()

    flash(f'{username} successfully deleted', 'success')
    return redirect('/users')


# flash messaging for email already in use when creating new user
# docstrings

@app.route('/users/<int:user_id>/posts/new')
def post_form(user_id):
    """Shows form to add a post for user with user_id"""
    user = User.query.get_or_404(user_id)
    return render_template('new_post.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """Adds post using 'add form' data and redirects to the user detail page"""
    title = request.form["title"]
    content = request.form["content"]
    created_by = int(user_id)

    new_post = Post(title=title, content=content, created_by=created_by)

    db.session.add(new_post)
    db.session.commit()

    flash(f'{new_post.title} successfully added', 'success')

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Shows post with id."""
    post = Post.query.get_or_404(post_id)
    
    return render_template('post.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """Shows form to edit post and to cancel edit (go back to user page)"""
    post = Post.query.get_or_404(post_id)

    return render_template('edit_post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """Handles post edit and table update in postgres. Redirects to the user view"""
    post = Post.query.get_or_404(post_id)

    title = request.form["title"]
    content = request.form["content"]

    post.title = title
    post.content = content

    db.session.commit()

    flash('Edit successful', 'success')

    return redirect(f'/users/{post.created_by}')

@app.route('/posts/<int:post_id>/delete')
def post_delete(post_id):
    """Deletes post with id. Redirects back to user page."""
    post = Post.query.get_or_404(post_id)
    user_id = post.created_by
    title = post.title
    db.session.delete(post)
    db.session.commit()

    flash(f'{title} successfully deleted', 'success')

    return redirect(f'/users/{user_id}')

@app.errorhandler(404)
def page_not_found(e):
    render_template('404.html'), 404
    
