"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
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
    tags = Tag.query.all()
    return render_template('new_post.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """Adds post using 'add form' data and redirects to the user detail page"""
    title = request.form["title"]
    content = request.form["content"]
    created_by = int(user_id)
    tags = request.form.getlist('tags')

    new_post = Post(title=title, content=content, created_by=created_by)

    db.session.add(new_post)
    db.session.commit()

    for tag in tags:
        t = Tag.query.filter(Tag.name == tag).all()
        new_post.tags.append(t[0])

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
    tags = Tag.query.all()

    return render_template('edit_post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """Handles post edit and table update in postgres. Redirects to the user view"""
    post = Post.query.get_or_404(post_id)

    title = request.form["title"]
    content = request.form["content"]
    tags = request.form.getlist("tags")
    for tag in tags:
        t = Tag.query.filter(Tag.name == tag).all()
        post.tags.append(t[0])

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

@app.route('/tags')
def tags():
    """Lists all tags with links to the tag detail page and associated posts.
    Provides option to add a new tag"""
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_posts(tag_id):
    """Gives any details about tag and lists all associated posts.
    Provides option to edit or delete tag"""
    tag = Tag.query.get(tag_id)
    posts = tag.posts
    return render_template('tag_details.html', tag=tag, posts=posts)

@app.route('/tags/new')
def new_tag_form():
    """Shows form to add new tag"""
    return render_template('add_tag.html')

@app.route('/tags/new', methods=["POST"])
def add_tag():
    """Process new tag form data and add tag to db. Redirect to tag list page"""
    
    name = request.form['name']
    new_tag = Tag(name=name)
    try:
        db.session.add(new_tag)
        db.session.commit()

        flash(f'{name} tag successfully created', 'success')
        return redirect('/tags')

    except exc.IntegrityError:
        flash(f'{name} already created', 'error')
        return redirect('/tags/new')

@app.route('/tags/<int:tag_id>/edit')
def tag_edit_form(tag_id):
    """Shows form to edit tag"""
    tag = Tag.query.get(tag_id)

    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tag_edit(tag_id):
    """Process edit form data to update form in db. Redirect to tag list page"""
    tag = Tag.query.get(tag_id)
    name = request.form['name']
    tag.name = name

    db.session.commit()

    flash(f'{tag.name} successfully updated', 'success')
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tag_delete(tag_id):
    """Delete tag from db"""

# make sure cannot delete tag if post still attached to it. tag must be removed from post first
# make flash saying so