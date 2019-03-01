from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Required

class Blog_postForm(FlaskForm):
   
    author = TextAreaField('author', validators=[Required()])
    quote = SubmitField('upvote',validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):

    comment= TextAreaField('comment', validators=[Required()])
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')