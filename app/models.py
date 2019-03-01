from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Quote:

    all_quotes = []

    def __init__(self,id,author,quote,permalink):
        self.id =id
        self.author = author
        self.quote = quote
        self.permalink = "http:\/\/quotes.stormconsultancy.co.uk\/quotes\/38" 
        
    def save_quotes(self):
       Quote.all_quotes.append(self)


    @classmethod
    def clear_quotes(cls):
       Post.all_quotes.clear()

    @classmethod
    def get_quotes(cls,id):

        response = []

        for Quote in cls.all_quotes:
            if Quote.user_id == id:
                response.append(quote)

        return response

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    post = db.relationship('Blog_post',backref = 'user',lazy="dynamic")
    comment = db.relationship('Comment',backref = 'user',lazy="dynamic")
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure  = db.Column(db.String(255))


   
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)
    def __repr__(self):
        return f'User {self.username}'
        
    
class Blog_post(db.Model):

    __tablename__ = 'post'

    id = db.Column(db.Integer,primary_key = True)
    author = db.Column(db.String(255))
    quote = db.Column(db.String(255))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    comment = db.relationship('Comment',backref = 'post',lazy="dynamic")

    def save_posts(self):
        db.session.add(self)
        db.session.commit()
 
    @classmethod
    def get_posts(id):
        posts = Blog_post.query.all()
        return posts

    def __repr__(self):
        return f'User {self.name}'


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    description= db.Column(db.String(255))
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    def __repr__(self):
        return f'User {self.name}'

    def save_comments(self):
       db.session.add(self)
       db.session.commit()
     
    @classmethod
    def get_comments(id):
        posts = post.query.all()
        return posts





 