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

    def __init__(self,id,author,quote):
        self.id =id
        self.author = author
        self.quote = quote
     
        
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
    post = db.relationship('Blog',backref = 'user',lazy="dynamic")
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
        
    
class Blog(db.Model):

    __tablename__ = 'blogs'

    id = db.Column(db.Integer,primary_key = True)
    blog = db.Column(db.String(255))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    comment = db.relationship('Comment',backref = 'blogs',lazy="dynamic")
    
    def save_blogs(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_blogs(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_blogs(id):
        blogs = Blog.query.filter_by(id=user_id).all()
        return blogs

    def __repr__(self):
        return f'User {self.name}'


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    description= db.Column(db.String(255))
    blogs_id = db.Column(db.Integer,db.ForeignKey('blogs.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    
    def save_comments(self):
       db.session.add(self)
       db.session.commit()
     
    def delete_comments(self):
       db.session.add(self)
       db.session.commit()

    @classmethod
    def get_comments(id):
       comments = Comment.query.all()
       return comments

    

class Subscribe(db.Model):
    __tablename__= 'subscribe'

    id = db.Column(db.Integer,primary_key = True)
    email= db.Column(db.String(255))
    name = db.Column(db.String(255))

    
    def __repr__(self):
        return f'User {self.email}'

    def save_subscribe(self):
       db.session.add(self)
       db.session.commit()

    @classmethod
    def get_subscribe(id):
       subscribe = Subscribe.query.all()
       return subscribe



 