from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import BlogForm,UpdateProfile,CommentForm,SubscribeForm
from ..models import  User,Blog,Comment,Subscribe
from flask_login import login_required,current_user
from .. import db,photos
from ..request import get_quotes
from ..email import mail_message

# Pitch = pitch.Pitch

@main.route('/')
def index():
    """ View root page function that returns index page
    """
    

    title = 'Home- Welcome'
    all_blogs = Blog.query.all()
    quote=get_quotes()
    return render_template('index.html', title = title,all_blogs=all_blogs, quote= quote)

def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

    
@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)

@main.route('/new_blog', methods=['GET', 'POST'])
@login_required
def new_blog():
    blog_form = BlogForm()
    
    if blog_form.validate_on_submit():
        
        blog = blog_form.blog.data
        # user_id = blog_form.user_id.data
        new_blog = Blog(blog=blog,user_id=current_user.id)
        new_blog.save_blogs() 
        subscriber=Subscribe.query.all()
        for subscribe in subscriber:
            mail_message("New Blog Post","email/welcome_user",subscribe.email, new_blog = new_blog )
        return redirect(url_for('main.index'))

    return render_template('new_blog.html', blog_form=blog_form)

@main.route('/comment/new/<int:id>', methods=['GET', 'POST'])
@login_required
def comment(id):
    comment_form = CommentForm()
    
    blog= Blog.query.filter_by(id=id).first()
    if comment_form.validate_on_submit():
        description = comment_form.description.data
        # user_id = comment_form.user_id.data
        new_comment = Comment(description=description, blogs_id  = id, user_id=current_user.id)
        new_comment.save_comments()
        new_comment.delete_comments()
        return redirect(url_for('main.index'))

    return render_template('comment.html',comment_form=comment_form, blog= blog)

@main.route('/subscribe',methods=["GET","POST"])
def subscribe():
    form=SubscribeForm()

    if form.validate_on_submit():
        email = form.email.data
        subscribe = Subscribe(email=form.email.data)
        db.session.add(subscribe)
        db.session.commit()

        
        mail_message("New Blog Post","email/welcome_user",subscribe.email)
        return redirect(url_for('main.index'))

        title = 'Subscribe'
    return render_template('subscribe.html',form=form)

@main.route('/delete/comment/<int:id>', methods = ['GET', 'POST'])
@login_required
def delete_comment(id):
  form=CommentForm()
  comment=Comment.query.filter_by(id=id).first()
 
  if comment is not None:
     comment.delete_comments()
     return redirect(url_for('main.index'))
     return render_template('comment.html', form=form)

@main.route('/delete/post/<int:id>', methods = ['GET', 'POST'])
@login_required
def delete_blogs(id):
    blog=Blog.query.filter_by(id=id).first()
 

    if blog is not None:
       blog.delete_blogs()
       return redirect(url_for('main.index'))