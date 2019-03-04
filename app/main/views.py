from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import BlogForm,UpdateProfile,CommentForm
from ..models import  User,Blog,Comment
from flask_login import login_required,current_user
from .. import db,photos
from ..request import get_quotes


# Pitch = pitch.Pitch

@main.route('/')
def index():
    """ View root page function that returns index page """
    # # Getting categiries of pitch
    # pickup_lines = get_movies('pickup lines')
    # interview_pitch = get_movies('interview pitch')
    # product_pitch = get_movies('now_playing')
    # promotion_pitch = get_movies('promotion pitch')

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

    return render_template("profile/profile.html", user=user,pitch_form=pitch_form)

@main.route('/new', methods=['GET', 'POST'])
@login_required
def new_blog():
    blog_form = BlogForm()
    
    if post_form.validate_on_submit():
        
        blog = blog_form.blog.data
        user_id = post_form.user_id.data
        new_post = Post(blog=quote,user_id=current_user.id)
        new_post.save_post() 
    
        return redirect(url_for('main.index'))

    return render_template('new_pitch.html', pitch_form=pitch_form)

@main.route('/comment/new', methods=['GET', 'POST'])
@login_required
def comment(id):
    comment_form = CommentForm()
    
    post= Blog.query.get(id)

    if comment_form.validate_on_submit():
        comment = comment_form.comment.data
        
        new_comment = Comment(comment=comment,user_id=user_id)
        new_comment.save_comment()
        return redirect(url_for('main.index'))

    return render_template('comment.html',comment_form=comment_form)
    
@main.route('/vote', methods=['POST'])
def vote():
    data = simplejson.loads(request.data)
    update_item(c, [data['member']])
    output = select_all_items(c, [data['member']])
    pusher.trigger(u'poll', u'vote', output)
    return request.data