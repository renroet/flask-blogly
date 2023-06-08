from unittest import TestCase
from app import app
from flask import session
from sqlalchemy import delete
from models import User, Post, db

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_tests'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class FlaskTests(TestCase):
    """Tests for views in Users"""

    def setUp(self): 
        """Clears user table and then adds a sample user"""
        Post.query.delete()
        User.query.delete()

        user = User(first_name="Kieren", last_name="Kooy", email="something.com")
        post = Post(title='Hello', content="World")

        db.session.add(user)
        db.session.commit()

        db.session.add(post)
        db.session.commit()

        self.user_id = user.id 
        self.post_id = post.id
        print(self.post_id)
    
    def tearDown(self):
        """Cleans up after each function to the previous session status"""
        db.session.rollback()

    # def setUp(self) -> None:
    #     return super().setUp()

    def test_redirect(self):
        with app.test_client() as client:
            resp = client.get('/', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Kieren", html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "Howard", "last_name": "Bruxton", "email": "sirfancyname@knightly.com", "image_url": ""}
            resp = client.post(f'/users/new', data = d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Howard", html)

    def test_details(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Kooy</div></h1>", html)

    def test_edit_user(self):
         with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id + 1}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 404)
            
    def test_add_post(self):
        with app.test_client() as client:
            d = {"title": "A Good Day", "content": "To you all"}
            resp = client.post(f'/users/{self.user_id}/posts/new', data = d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("A Good Day", html)
        
    # def test_delete_post(self):
    #     with app.test_client() as client:
    #         post = Post.query.get(self.post_id)
    #         d = {f"{k}":f"{v}" for (k,v) in post.items()}

    #         resp = client.post(f'/posts/{self.post_id}/delete', data = d, follow_redirects=True)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertNotIn("Hello", html)
    
